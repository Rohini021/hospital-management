from pymongo import MongoClient
import datetime
import jwt
from utils import *

CONN_STRING = "localhost:27017"
client = MongoClient(CONN_STRING)
auth_data_collection = client.hospital.authData
doctor_collection = client.hospital.doctors
patient_collection = client.hospital.patients
jwt_secret = "hospitalsecret"

def register_user_service(user_data):
    try:
        user_data_from_db = auth_data_collection.find_one({"contact_number":user_data["contact_number"]})
        if user_data_from_db:
            return "User with given contact number already present", 400
        user_data["user_id"] = generate_unique_id(8)
        auth_data_collection.insert_one(user_data)
        return "User registered successfully!", 200
    except Exception as exc:
        print("exception occured: ", str(exc))
        return "exception occured: "+ str(exc), 400

def login_user_service(login_data):
    data = dict()
    try:
        user = auth_data_collection.find_one(login_data)
        if user:
            payload = {
                        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
                        'user_id': user.get("user_id"),
                        'role': user.get("role")
                    }
            token = jwt.encode(payload, jwt_secret)
            data["contact_number"] = login_data.get("contact_number")
            data["token"] = token.decode('UTF-8')
            data["duration"] = 30
            return data, 200
        else:
            return "Login failed for provided credentials", 400
    except Exception as exc:
        print("exception occured: ", str(exc))
        return "exception occured: "+ str(exc), 400

def get_slots(doctor_id, date, request_headers):
    try:
        print("get doctors slots")
        data = jwt.decode(request_headers.get("token"), jwt_secret)
        role = data["role"]
        if role == "doctor" or role == "admin":
            data = doctor_collection.find_one({"user_id":doctor_id, "date":date}, {"_id":0})
        elif role == "patient":
            data = doctor_collection.find_one({"user_id":doctor_id, "date":date}, {"_id":0, "appointments.patient_id":0})
        return data, 200
    except Exception as exc:
        print("exception occured: ", str(exc))
        return "exception occured: "+ str(exc), 400
    
def book_appointment(doctor_id, date, slot, request_headers):
    try:
        print("book appointment")
        data = jwt.decode(request_headers.get("token"), jwt_secret)
        role = data["role"]
        user_id = data["user_id"]
        if role == "doctor" or role == "admin":
            return "only patient users can book appointment", 400
        doctor_data = doctor_collection.find_one({"user_id":doctor_id, "date":date}, {"_id":0})
        latest_appointment = dict()
        latest_appointment["patient_id"] = user_id
        latest_appointment["slot"] = slot
        if doctor_data and len(doctor_data.get("appointments")) >= 12:
            return "This doctor has been already appointed for 12 other patients. Please book slot for other doctors", 400
        if doctor_data and doctor_data.get("appointments"):
            update_appointments = doctor_data.get("appointments")
            update_appointments.append(latest_appointment)
        else:
            update_appointments = [latest_appointment]
        doctor_collection.update_one({"user_id":doctor_id, "date":date},{'$set': {"appointments":update_appointments}}, upsert=True)
        patient_data = patient_collection.find_one({"user_id":user_id}, {"_id":0})
        if patient_data and patient_data.get("patients_appointments"):
            patients_appointments = patient_data.get("patients_appointments")
            patients_appointments.append({"doctor_id":doctor_id, "date":date, "slot":slot})
        else:
            patients_appointments = [{"doctor_id":doctor_id, "date":date, "slot":slot}]
        patient_collection.update_one({"user_id":user_id},{'$set':  {"patients_appointments":patients_appointments}}, upsert=True)
        return "success", 200
    except Exception as exc:
        print("exception occured: ", str(exc))
        return "exception occured: "+ str(exc), 400
    
def get_appointment_history(patient_id):
    try:
        print("get patient appointment history for: ", patient_id)
        data = patient_collection.find_one({"user_id":patient_id}, {"_id":0})
        if not data:
            return "no record found", 400
        return data, 200
    except Exception as exc:
        print("exception occured: ", str(exc))
        return "exception occured: "+ str(exc), 400
    
def cancel_appointment(doctor_id, patient_id, date):
    try:
        print("cancel appointment")
        doctor_data = doctor_collection.find_one({"user_id":doctor_id, "date":date}, {"_id":0})
        if doctor_data and doctor_data.get("appointments"):
            new_appointments = []
            old_appointments = doctor_data.get("appointments")
            for apt in old_appointments:
                if apt.get("patient_id") != patient_id:
                    new_appointments.append(apt)
            doctor_collection.update_one({"user_id":doctor_id, "date":date},{'$set': {"appointments":new_appointments}})

            patient_data = patient_collection.find_one({"user_id":patient_id}, {"_id":0})
            patients_appointments = patient_data.get("patients_appointments")
            new_appointments = []
            for apt in patients_appointments:
                if apt.get("doctor_id") != doctor_id and apt.get("date") == date:
                    new_appointments.append(apt)
            patient_collection.update_one({"user_id":patient_id},{'$set':  {"patients_appointments":new_appointments}})
            return "appointment cancelled", 200
    except Exception as exc:
        print("exception occured: ", str(exc))
        return "exception occured: "+ str(exc), 400
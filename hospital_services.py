from pymongo import MongoClient
import datetime
import jwt
from utils import *

CONN_STRING = "localhost:27017"
client = MongoClient(CONN_STRING)
auth_data_collection = client.hospital.authData
appointments_collection = client.hospital.appointments
doctor_collection = client.hospital.doctors
patient_collection = client.hospital.patients
doctor_appointment_summary_collection = client.hospital.doctorAppointmentsSummary

jwt_secret = "hospitalsecret"

slot_mapping = {
    "00.1":"00:00-00:15","00.2":"00:15-00:30","00.3":"00:30-00:45","00.4":"00:45-01:00",
    "01.1":"01:00-01:15","01.2":"01:15-01:30","01.3":"01:30-01:45","01.4":"01:45-02:00",
    "02.1":"02:00-02:15","02.2":"02:15-02:30","02.3":"02:30-02:45","02.4":"02:45-03:00",
    "03.1":"03:00-03:15","03.2":"03:15-03:30","03.3":"03:30-03:45","03.4":"03:45-04:00",
    "04.1":"04:00-04:15","04.2":"04:15-04:30","04.3":"04:30-04:45","04.4":"04:45-05:00",
    "05.1":"05:00-05:15","05.2":"05:15-05:30","05.3":"05:30-05:45","05.4":"05:45-06:00",
    "06.1":"06:00-06:15","06.2":"06:15-06:30","06.3":"06:30-06:45","06.4":"06:45-07:00",
    "07.1":"07:00-07:15","07.2":"07:15-07:30","07.3":"07:30-07:45","07.4":"07:45-08:00",
    "08.1":"08:00-08:15","08.2":"08:15-08:30","08.3":"08:30-08:45","08.4":"08:45-09:00",
    "09.1":"09:00-09:15","09.2":"09:15-09:30","09.3":"09:30-09:45","09.4":"09:45-10:00",
    "10.1":"10:00-10:15","10.2":"10:15-10:30","10.3":"10:30-10:45","10.4":"10:45-11:00",
    "11.1":"11:00-11:15","11.2":"11:15-11:30","11.3":"11:30-11:45","11.4":"11:45-12:00",
    "12.1":"12:00-12:15","12.2":"12:15-12:30","12.3":"12:30-12:45","12.4":"12:45-13:00",
    "13.1":"13:00-13:15","13.2":"13:15-13:30","13.3":"13:30-13:45","13.4":"13:45-14:00",
    "14.1":"14:00-14:15","14.2":"14:15-14:30","14.3":"14:30-14:45","14.4":"14:45-15:00",
    "15.1":"15:00-15:15","15.2":"15:15-15:30","15.3":"15:30-15:45","15.4":"15:45-16:00",
    "16.1":"16:00-16:15","16.2":"16:15-16:30","16.3":"16:30-16:45","16.4":"16:45-17:00",
    "17.1":"17:00-17:15","17.2":"17:15-17:30","17.3":"17:30-17:45","17.4":"17:45-18:00",
    "18.1":"18:00-18:15","18.2":"18:15-18:30","18.3":"18:30-18:45","18.4":"18:45-19:00",
    "19.1":"19:00-19:15","19.2":"19:15-19:30","19.3":"19:30-19:45","19.4":"19:45-20:00",
    "20.1":"20:00-20:15","20.2":"20:15-20:30","20.3":"20:30-20:45","20.4":"20:45-21:00",
    "21.1":"21:00-21:15","21.2":"21:15-21:30","21.3":"21:30-21:45","21.4":"21:45-22:00",
    "22.1":"22:00-22:15","22.2":"22:15-22:30","22.3":"22:30-22:45","22.4":"22:45-23:00",
    "23.1":"23:00-23:15","23.2":"23:15-23:30","23.3":"23:30-23:45","23.4":"23:45-00:00"
}

def register_user_service(user_data):
    try:
        user_data_from_db = auth_data_collection.find_one({"contact_number":user_data["contact_number"]})
        if user_data_from_db:
            return "User with given contact number already present", 400
        unique_id = generate_unique_id(8)
        
        #for clarification contacating role with unique id
        if user_data["role"] == "doctor":
            if not user_data.get("specialty"):
                return "please provide specialty", 400
            user_data["user_id"] = "doctor_"+unique_id
        elif user_data["role"] == "admin":
            user_data["user_id"] = "admin_"+unique_id
        elif user_data["role"] == "patient":
            user_data["user_id"] = "patient_"+unique_id
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

def list_doctors():
    try:
        print("list all doctors")
        cursor = auth_data_collection.find({"role":"doctor"}, {"user_id":1, "name":1,"_id":0})
        data = []
        for dt in cursor:
            data.append(dt)
        return data, 200
    except Exception as exc:
        print("exception occured: ", str(exc))
        return "exception occured: "+ str(exc), 400

def get_doctor_details(doctor_id):
    try:
        print("list all doctors")
        data = auth_data_collection.find_one({"user_id":doctor_id}, {"_id":0, "password":0})
        return data, 200
    except Exception as exc:
        print("exception occured: ", str(exc))
        return "exception occured: "+ str(exc), 400

def get_slots(doctor_id, date, request_headers):
    try:
        print("get doctors slots")
        data = jwt.decode(request_headers.get("token"), jwt_secret)
        role = data["role"]
        if role == "admin" or role == "doctor":
            cursor = appointments_collection.find({"doctor_id":doctor_id, "date":date}, {"_id":0})
        elif role == "patient":
            cursor = appointments_collection.find({"doctor_id":doctor_id, "date":date}, {"_id":0, "patient_id":0, "total_time_for_patient":0})
        appointed_data = []
        cancelled_data = []
        slots_appointed = []
        for dt in cursor:
            if dt["status"] == "active":
                appointed_data.append(dt)
                slots_appointed.extend(dt["slots"])
            elif dt["status"] == "cancelled":
                cancelled_data.append(dt)
        available_slots = {key: slot_mapping[key] for key in slot_mapping if key not in slots_appointed}
        return {"slots_available":available_slots, "appointed_slots": appointed_data, "cancelled_slots": cancelled_data}, 200
    except Exception as exc:
        print("exception occured: ", str(exc))
        return "exception occured: "+ str(exc), 400

def list_appoinements(date):
    try:
        cur = appointments_collection.find({"date":date},{"_id":0})
        apts = []
        for cr in cur:
            apts.append(cr)
        return apts, 200
    except Exception as exc:
        print("exception occured: ", str(exc))
        return "exception occured: "+ str(exc), 400
def view_appoinement(appointment_id, request_headers):
    try:
        print("get appointment details for id: ", appointment_id)
        data = jwt.decode(request_headers.get("token"), jwt_secret)
        logged_in_user = data["user_id"]
        role = data["role"]
        apt_data = appointments_collection.find_one({"appointment_id":appointment_id}, {"_id":0})
        print("1111", apt_data)
        #the patient who booked the appointment can see the appointment details
        if role == "patient" and logged_in_user != apt_data["patient_id"]:
            return "patient who booked the appointment can see the appointment details", 400
        return apt_data, 200
    except Exception as exc:
        print("exception occured: ", str(exc))
        return "exception occured: "+ str(exc), 400

def book_appointment(doctor_id, date, slots, request_headers):
    try:
        print("book appointment")
        # Patients can book an appointment with a doctor for max duration of 2 Hours
        # 2 hours duration means max 8 slots allowed, as 1 slot is equal to 15 minutes
        if len(slots) > 8:
            return "Patients can book an appointment with a doctor for max duration of 2 Hours", 400
        data = jwt.decode(request_headers.get("token"), jwt_secret)
        role = data["role"]
        logged_in_user = data["user_id"]
        if role == "doctor" or role == "admin":
            return "only patient users can book appointment", 400
        doctor_appointments_of_day_cursor = appointments_collection.find({"doctor_id":doctor_id, "date":date})
        total_apt = []
        for apt in doctor_appointments_of_day_cursor:
            total_apt.append(apt)
        if len(total_apt) >= 12:
            # Doctors are expected to have a maximum of 12 different patients
            return "This doctor has been already appointed for 12 other patients. Please book slot for other doctor", 400
        doctor_appointment_summary = doctor_appointment_summary_collection.find_one({"doctor_id":doctor_id, "date":date})
        if doctor_appointment_summary:
            # Doctors are expected to have a maximum of 8 hours (480 minutes) maximum total appointments per day
            if doctor_appointment_summary["total_time_for_day"] >= 480:
                return "This doctor has been already appointed for 8 hours for today. Please book slot for other doctor", 400
        
        #check if slots are overlapping
        if doctor_appointment_summary:
            if any(True for x in slots if x in doctor_appointment_summary["total_slots_appointed"]):
                return "check if any of selected slot is already booked", 400
        appointment_data = dict()
        appointment_data["appointment_id"] = generate_unique_id(4)
        appointment_data["doctor_id"] = doctor_id
        appointment_data["date"] = date
        appointment_data["slots"] = slots
        appointment_data["patient_id"] = logged_in_user
        appointment_data["status"] = "active"
        appointment_data["total_time_for_patient"] = len(slots)* 15
        appointments_collection.insert_one(appointment_data)
        if doctor_appointment_summary:
            total_time_for_day = doctor_appointment_summary.get("total_time_for_day") + appointment_data["total_time_for_patient"]
            total_appointment_count_for_day = doctor_appointment_summary.get("total_appointment_count_for_day") + 1
            slots.extend(doctor_appointment_summary.get("total_slots_appointed"))
        else:
            total_time_for_day = appointment_data["total_time_for_patient"]
            total_appointment_count_for_day = 1
        doctor_appointment_summary_collection.update_one({"doctor_id":doctor_id, "date":date}, {"$set":{"total_time_for_day":total_time_for_day, "total_appointment_count_for_day":total_appointment_count_for_day, "total_slots_appointed":slots}}, upsert=True)
        return "success", 200
    except Exception as exc:
        print("exception occured: ", str(exc))
        return "exception occured: "+ str(exc), 400
    
def get_appointment_history(patient_id):
    try:
        print("get patient appointment history for: ", patient_id)
        data_cursor = appointments_collection.find({"patient_id":patient_id}, {"_id":0})
        data = []
        for patient in data_cursor:
            data.append(patient)
        if not data:
            return "no record found", 400
        return data, 200
    except Exception as exc:
        print("exception occured: ", str(exc))
        return "exception occured: "+ str(exc), 400
    
def cancel_appointment(doctor_id, patient_id, date):
    try:
        print("cancel appointment")
        data = appointments_collection.find_one({"doctor_id":doctor_id, "patient_id":patient_id, "date":date}, {"_id":0})
        if data:
            appointments_collection.update_one({"doctor_id":doctor_id, "patient_id":patient_id, "date":date}, { "$set":{"status":"cancelled"}})
            return "appointment cancelled", 200
        else:
            return "no record found", 400
    except Exception as exc:
        print("exception occured: ", str(exc))
        return "exception occured: "+ str(exc), 400
    
def get_doctors_exceeding_6_hours(date, request_headers):
    try:
        data = jwt.decode(request_headers.get("token"), jwt_secret)
        role = data["role"]
        if role != "admin":
            return "Only admin can check list of doctors exceeding 6 hours of appointment", 400
        # view doctors who have 6+ hours (360 minutes) total appointments in a day
        data_cur = doctor_appointment_summary_collection.find({"total_time_for_day":{"$gte":360},"date":date})
        doctors_data = []
        for data in data_cur:
            data['_id'] = str(data['_id'])
            doctors_data.append(data)
        print(doctors_data)
        return doctors_data, 200
    except Exception as exc:
        print("exception occured: ", str(exc))
        return "exception occured: "+ str(exc), 400

def get_doctor_with_most_appointments(date, request_headers):
    try:
        data = jwt.decode(request_headers.get("token"), jwt_secret)
        role = data["role"]
        if role != "admin":
            return "Only admin can check doctor with most appointments", 400
        data_cur = doctor_appointment_summary_collection.find({"date":date},{"doctor_id":1, "total_appointment_count_for_day":1, "_id":0}).sort("total_appointment_count_for_day",-1)
        data = []
        for dt in data_cur:
            data.append(dt)
        result = dict()
        result["doctor_with_most_appointments"] = data[0]
        result["sorted_list"] = data
        return result, 200
    except Exception as exc:
        print("exception occured: ", str(exc))
        return "exception occured: "+ str(exc), 400
    
def get_availability(date):
    try:
        dr_cursor = auth_data_collection.find({"role":"doctor"}, {"user_id":1, "_id":0})
        all_dr = []
        for dr in dr_cursor:
            all_dr.append(dr["user_id"])
        cursor = doctor_appointment_summary_collection.find({"date":date}, {"total_slots_appointed":1, "doctor_id":1,"_id":0})
        all_doctors_slots = []
        for dt in cursor:
            all_dr.remove(dt["doctor_id"])
            result = {key: slot_mapping[key] for key in slot_mapping if key not in dt["total_slots_appointed"]}
            all_doctors_slots.append({"doctor_id":dt["doctor_id"], "slots_available":result})
        for dr in all_dr:
            all_doctors_slots.append({"doctor_id":dt["doctor_id"], "slots_available": slot_mapping})
        return all_doctors_slots, 200
    except Exception as exc:
        print("exception occured: ", str(exc))
        return "exception occured: "+ str(exc), 400

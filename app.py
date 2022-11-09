from flask import Flask, request
import jwt
import hospital_services
from utils import *
from functools import wraps


app = Flask(__name__)
jwt_secret = "hospitalsecret"
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('token')
        print("wwwww", token)
        try:
            data = jwt.decode(token, jwt_secret)
            print("aaaaa", data)
        except:
            return "invalid token", 403
        return f(*args, **kwargs)
    return decorated

@app.route('/hospital-management/register_user', methods=['POST'])
def register_user():
    try:
        request_data = request.json
        print("Request data for register user: ", request_data)
        data, code = hospital_services.register_user_service(request_data)
        return create_response(code, data), code
    except Exception as exc:
        print("exception occured:: ", str(exc))
        return create_response(400, {"error": str(exc)}), 400
    
@app.route('/hospital-management/login', methods=['POST'])
def user_login():
    try:
        request_data = request.json
        print("Request data for login user: ", request_data)
        data, code = hospital_services.login_user_service(request_data)
        return create_response(code, data), code
    except Exception as exc:
        print("exception occured:: ", str(exc))
        return create_response(400, {"error": str(exc)}), 400

@app.route('/hospital-management/doctors/<doctor_id>/<date>/slots', methods=['GET'])
@token_required
def get_slots(doctor_id, date):
    try:
        data, code = hospital_services.get_slots(doctor_id, date, request.headers)
        return create_response(code, data), code
    except Exception as exc:
        print("exception occured:: ", str(exc))
        return create_response(400, {"error": str(exc)}), 400

@app.route('/hospital-management/book_appointment/<doctor_id>/<date>/<slot>', methods=['POST'])
@token_required
def book_appointment(doctor_id, date, slot):
    try:
        data, code = hospital_services.book_appointment(doctor_id, date, slot, request.headers)
        return create_response(code, data), code
    except Exception as exc:
        print("exception occured:: ", str(exc))
        return create_response(400, {"error": str(exc)}), 400

@app.route('/hospital-management/get_appointment_history/<patient_id>', methods=['GET'])
@token_required
def get_appointment_history(patient_id):
    try:
        data, code = hospital_services.get_appointment_history(patient_id)
        return create_response(code, data), code
    except Exception as exc:
        print("exception occured:: ", str(exc))
        return create_response(400, {"error": str(exc)}), 400

@app.route('/hospital-management/cancel_appointment/<doctor_id>/<patient_id>/<date>', methods=['DELETE'])
@token_required
def cancel_appointment(doctor_id, patient_id, date):
    try:
        data, code = hospital_services.cancel_appointment(doctor_id, patient_id, date)
        return create_response(code, data), code
    except Exception as exc:
        print("exception occured:: ", str(exc))
        return create_response(400, {"error": str(exc)}), 400

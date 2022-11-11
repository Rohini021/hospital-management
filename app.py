from flask import Flask, request
import jwt
import hospital_services
from utils import *
from functools import wraps
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Seans-Python-Flask-REST-Boilerplate"
    }
)

app = Flask(__name__)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

jwt_secret = "hospitalsecret"
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('token')
        try:
            data = jwt.decode(token, jwt_secret)
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

@app.route('/hospital-management/doctors', methods=['GET'])
def list_doctors():
    try:
        data, code = hospital_services.list_doctors()
        return create_response(code, data), code
    except Exception as exc:
        print("exception occured:: ", str(exc))
        return create_response(400, {"error": str(exc)}), 400

@app.route('/hospital-management/doctors/<doctor_id>', methods=['GET'])
def get_doctor_details(doctor_id):
    try:
        data, code = hospital_services.get_doctor_details(doctor_id)
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

@app.route('/hospital-management/appoinements/<date>', methods=['GET'])
@token_required
def list_appoinements(date):
    try:
        data, code = hospital_services.list_appoinements(date)
        return create_response(code, data), code
    except Exception as exc:
        print("exception occured:: ", str(exc))
        return create_response(400, {"error": str(exc)}), 400

@app.route('/hospital-management/view_appoinement/<appointment_id>', methods=['GET'])
@token_required
def view_appoinement(appointment_id):
    try:
        data, code = hospital_services.view_appoinement(appointment_id, request.headers)
        return create_response(code, data), code
    except Exception as exc:
        print("exception occured:: ", str(exc))
        return create_response(400, {"error": str(exc)}), 400

@app.route('/hospital-management/book_appointment/<doctor_id>/<date>', methods=['POST'])
@token_required
def book_appointment(doctor_id, date):
    try:
        slots = request.json.get("slots")
        data, code = hospital_services.book_appointment(doctor_id, date, slots, request.headers)
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

@app.route('/hospital-management/get_doctors_exceeding_6_hours/<date>', methods=['GET'])
@token_required
def get_doctors_exceeding_6_hours(date):
    try:
        data, code = hospital_services.get_doctors_exceeding_6_hours(date, request.headers)
        return create_response(code, data), code
    except Exception as exc:
        print("exception occured:: ", str(exc))
        return create_response(400, {"error": str(exc)}), 400

@app.route('/hospital-management/get_doctor_with_most_appointments/<date>', methods=['GET'])
@token_required
def get_doctor_with_most_appointments(date):
    try:
        data, code = hospital_services.get_doctor_with_most_appointments(date, request.headers)
        return create_response(code, data), code
    except Exception as exc:
        print("exception occured:: ", str(exc))
        return create_response(400, {"error": str(exc)}), 400

@app.route('/hospital-management/get_availability/<date>', methods=['GET'])
@token_required
def get_availability(date):
    try:
        data, code = hospital_services.get_availability(date)
        return create_response(code, data), code
    except Exception as exc:
        print("exception occured:: ", str(exc))
        return create_response(400, {"error": str(exc)}), 400

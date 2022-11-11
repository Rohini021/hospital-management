import unittest
import mock
import hospital_services

user_data = {
                "name":"test",
                "contact_number": 00000,
                "password":"test",
                "role":"doctor",
                "address":"abc",
                "city":"abc",
                "country":"abc",
                "specialty":"Dermatologists"
            }

class TestHospitalServiceMethos(unittest.TestCase):

    @mock.patch('pymongo.collection.Collection.insert_one')
    def test_register_user_service(self, mock_insert):
        data , _ = hospital_services.register_user_service(user_data)
        self.assertEqual(data, "User registered successfully!")

    @mock.patch('pymongo.collection.Collection.insert_one')
    @mock.patch('pymongo.collection.Collection.find_one')
    def test_register_user_service_failure(self, mock_find, mock_insert):
        mock_find.return_value = user_data
        data, _ = hospital_services.register_user_service(user_data)
        self.assertEqual(data, "User with given contact number already present")


    @mock.patch('pymongo.collection.Collection.find_one')
    def test_login_user_service(self, mock_find):
        user_data = {
                        "contact_number": 00000000,
                        "password":"test"
                    }
        mock_find.return_value = user_data
        data, code = hospital_services.login_user_service(user_data)
        self.assertEqual(code, 200)

    @mock.patch('pymongo.collection.Collection.find_one')
    def test_login_user_service_failure(self, mock_find):
        user_data = {
                        "contact_number": 00000000,
                        "password":"test"
                    }
        mock_find.return_value = {}
        data, _ = hospital_services.login_user_service(user_data)
        self.assertEqual(data, "Login failed for provided credentials")

    @mock.patch('pymongo.collection.Collection.find')
    def test_list_doctors(self, mock_find):
        mock_find.return_value =[{"name": "n1","user_id": "doctor_NVU9ZA8Z1"},
                                 {"name": "n2","user_id": "doctor_NVU9ZA8Z2"}]
        data, code = hospital_services.list_doctors()
        self.assertEqual(code, 200)

    @mock.patch('pymongo.collection.Collection.find_one')
    def test_get_doctor_details(self, mock_find):
        test_data = {
                    "address": "abc",
                    "city": "abc",
                    "contact_number": 00000,
                    "country": "abc",
                    "name": "n1",
                    "role": "doctor",
                    "specialty": "Cardiologists",
                    "user_id": "doctor_NVU9ZA8Z"
                }
        mock_find.return_value = test_data
        data,_ = hospital_services.get_doctor_details("doctor_NVU9ZA8Z1")
        self.assertEqual(data, test_data)

    @mock.patch('pymongo.collection.Collection.find_one')
    @mock.patch('jwt.decode')
    def test_get_slots(self, mock_jwt, mock_find):
        mock_find.return_value = [{
                    "doctor_id": "doctor_NVU9ZA8Z",
                    "date": "11-11-2022",
                    "slots": [ "14.1"],
                    "patient_id": "patient_U2253EDE",
                    "status": "cancelled",
                    "total_time_for_patient": 15,
                    "appointment_id": "S6WJ"
                }]
        mock_jwt.return_value = {
            "user_id":"test",
            "role":"admin"
        }
        data,code = hospital_services.get_slots("doctor_NVU9ZA8Z1", "11-11-2022", {})
        self.assertEqual(code, 200)
        
    @mock.patch('pymongo.collection.Collection.find_one')
    def test_list_appoinements(self, mock_find):
        mock_find.return_value = {
                    "doctor_id": "doctor_NVU9ZA8Z",
                    "date": "11-11-2022",
                    "slots": [ "14.1"],
                    "patient_id": "patient_U2253EDE",
                    "status": "cancelled",
                    "total_time_for_patient": 15,
                    "appointment_id": "S6WJ"
                }
        data,code = hospital_services.list_appoinements("11-11-2022")
        self.assertEqual(code, 200)

    @mock.patch('pymongo.collection.Collection.find_one')
    @mock.patch('jwt.decode')
    def test_view_appoinement(self, mock_jwt, mock_find):
        mock_find.return_value = {
                    "doctor_id": "doctor_NVU9ZA8Z",
                    "date": "11-11-2022",
                    "slots": [ "14.1"],
                    "patient_id": "patient_U2253EDE",
                    "status": "cancelled",
                    "total_time_for_patient": 15,
                    "appointment_id": "S6WJ"
                }
        mock_jwt.return_value = {
            "user_id":"test",
            "role":"admin"
        }
        data,code = hospital_services.view_appoinement("apt_id", {})
        self.assertEqual(code, 200)

    @mock.patch('pymongo.collection.Collection.find_one')
    @mock.patch('jwt.decode')
    def test_view_appoinement_failure(self, mock_jwt, mock_find):
        mock_find.return_value = {
                    "doctor_id": "doctor_NVU9ZA8Z",
                    "date": "11-11-2022",
                    "slots": [ "14.1"],
                    "patient_id": "patient_U2253EDE",
                    "status": "cancelled",
                    "total_time_for_patient": 15,
                    "appointment_id": "S6WJ"
                }
        mock_jwt.return_value = {
            "user_id":"test",
            "role":"patient"
        }
        data,code = hospital_services.view_appoinement("apt_id", {})
        self.assertEqual(data, 'patient who booked the appointment can see the appointment details')

    @mock.patch('pymongo.collection.Collection.find_one')
    @mock.patch('pymongo.collection.Collection.insert_one')
    @mock.patch('pymongo.collection.Collection.update_one')
    def test_book_appointment_fali1(self, mock_insert, mock_update, mock_find):
        data,code = hospital_services.book_appointment("dr_id", "11-11-2022", ["11.1","11.2","11.2","11.4","12.1","12.2","12.3","12.4","13.1"], {})
        self.assertEqual(data, 'Patients can book an appointment with a doctor for max duration of 2 Hours')

    @mock.patch('jwt.decode')
    @mock.patch('pymongo.collection.Collection.find_one')
    @mock.patch('pymongo.collection.Collection.insert_one')
    @mock.patch('pymongo.collection.Collection.update_one')
    def test_book_appointment_fali1(self, mock_insert, mock_update, mock_find, mock_jwt):
        mock_find.return_value = {
                    "doctor_id": "doctor_NVU9ZA8Z",
                    "date": "11-11-2022",
                    "slots": [ "14.1"],
                    "patient_id": "patient_U2253EDE",
                    "status": "cancelled",
                    "total_time_for_patient": 15,
                    "appointment_id": "S6WJ",
                    "total_time_for_day":120,
                    "total_slots_appointed":["00.1","00.2"],
                    "total_appointment_count_for_day":1
                }
        mock_jwt.return_value = {
            "user_id":"test",
            "role":"patient"
        }
        data,code = hospital_services.book_appointment("dr_id", "11-11-2022", ["12.4,13.1"], {})
        self.assertEqual(data, 'success')

    @mock.patch('pymongo.collection.Collection.find')
    def test_get_appointment_history(self, mock_find):
        test_data = {
                    "doctor_id": "doctor_NVU9ZA8Z",
                    "date": "11-11-2022",
                    "slots": [ "14.1"],
                    "patient_id": "patient_U2253EDE",
                    "status": "cancelled",
                    "total_time_for_patient": 15,
                    "appointment_id": "S6WJ"}
        mock_find.return_value = test_data
        data,code = hospital_services.get_appointment_history("p_id")
        self.assertEqual(code, 200)
        
    @mock.patch('pymongo.collection.Collection.find_one')
    @mock.patch('pymongo.collection.Collection.update_one')
    def test_cancel_appointment(self, mock_update, mock_find):
        test_data = {
                    "doctor_id": "doctor_NVU9ZA8Z",
                    "date": "11-11-2022",
                    "slots": [ "14.1"],
                    "patient_id": "patient_U2253EDE",
                    "status": "cancelled",
                    "total_time_for_patient": 15,
                    "appointment_id": "S6WJ"}
        mock_find.return_value = test_data
        data,code = hospital_services.cancel_appointment("doctor_id", "patient_id", "11-11-2022")
        self.assertEqual(code, 200)
        
    @mock.patch('pymongo.collection.Collection.find')
    @mock.patch('jwt.decode')
    def test_get_doctors_exceeding_6_hours(self, mock_jwt, mock_find):
        mock_jwt.return_value = {
            "user_id":"test",
            "role":"admin"
        }
        test_data = {
                        "date": "11-11-2022",
                        "doctor_id": "doctor_NVU9ZA8Z",
                        "total_appointment_count_for_day": 2,
                        "total_slots_appointed": [
                            "14.3",
                            "14.2",
                            "14.4",
                            "14.1"
                        ],
                        "total_time_for_day": 60
                    }
        mock_find.return_value = test_data
        data,code = hospital_services.get_doctors_exceeding_6_hours("11-11-2022", {})
        self.assertEqual(code, 200)
        
if __name__ == '__main__':
    unittest.main()
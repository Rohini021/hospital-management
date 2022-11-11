# Hospital slots booking management

Simple flask APIs to manage slot bookings for hospital

## Installation
- configure mongodb: if configured locally, keep CONN_STRING (hospital_services.py) as it is else replace CONN_STRING in with your connection string to database.


- create virtual env:
```bash
python3 -m venv /<venv>
source <venv>/bin/activate
```

- clone the repository:
```bash
git clone https://github.com/Rohini021/hospital-management.git
```
- install requirement file:
```bash
pip3 install -r requirements.txt
```
- To locally run flask application run command:
```bash
FLASK_APP=app.py flask run
```
- Use provided postman collection or use swagger:
```bash
http://127.0.0.1:5000/swagger
```
## Deployment

Use docker image for deployment: rohini021/hospital_management:img3

Pull docker image with:
```bash
docker pull rohini021/hospital_management:img3
```

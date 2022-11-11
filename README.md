# Hospital slots booking management

Simple flask APIs to manage slot bookings for hospital

## Installation
- configure mongodb: if configured locally, keep CONN_STRING (hospital_services.py) as it is else replace CONN_STRING in with your connection string to database.


- create virtual env:
```bash
python3 -m venv /<path>/<venv_name>
cd /<path>
source <venv_name>/bin/activate
```

- clone the repository:
```bash
git clone https://github.com/Rohini021/hospital-management.git
cd hospital-management
```
- install requirement file:
```bash
pip3 install -r requirements.txt
```
- To locally run flask application run command:
```bash
FLASK_APP=app.py flask run
```
- Use provided postman collection (hospital_management_postman_collection.json) or use swagger:
```bash
http://127.0.0.1:5000/swagger
```
## Deployment

Use docker image for deployment: rohini021/hospital_management:img3

Pull docker image with:
```bash
docker pull rohini021/hospital_management:img3
```


![techUnicorn drawio](https://user-images.githubusercontent.com/25196773/201357682-d771b057-652e-4f0d-b5a8-26b0f4e69a7c.png)


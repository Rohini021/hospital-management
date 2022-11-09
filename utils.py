import string
import random

def generate_unique_id(size):
    '''
    generate unique id
    '''
    chars = list(set(string.ascii_uppercase + string.digits).difference('LIO01'))
    return ''.join(random.choices(chars, k=size))

def create_response(status_code, data):
    response = dict()
    response["StatusCode"] = status_code
    response["result"] = data
    return response
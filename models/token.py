from peewee import *
from .base import BaseModel
import random
import string
import yaml
import base64

with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

client_id = config['jwt']['client_id']

class ApiKey(BaseModel):
    id = IntegerField()
    client_id = CharField()
    client_secret = CharField()
    username = CharField()
    password = CharField()
    
    class Meta:
        db_table = 'apiKeys'
        

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def find_user(username: str):
    return list(ApiKey.select().where(ApiKey.username == username))


           
def create_user(username: str, password: str):
    user_obj = ApiKey(
        client_id = base64.b64encode(username.encode("ascii")),
        client_secret = get_random_string(30),
        username = username,
        password = password
    )
    
    user_obj.save()
    return user_obj

def generate_jwt(client_id:str, client_secret:str):
    username = base64.b64decode(client_id.encode("ascii"))
    userData = find_user(username)
    return userData
from peewee import *
from .base import BaseModel
from playhouse.shortcuts import model_to_dict
import random
import json
import string
import yaml
import jwt
import time

with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

client_id = config['jwt']['client_id']

def getTime():
    return str(time.time())[:10]

class ApiKey(BaseModel):
    id = IntegerField()
    client_id = CharField(max_length=30)
    client_secret = CharField(max_length=30)
    username = CharField(max_length=30)
    password = CharField(max_length=30)
    
    class Meta:
        db_table = 'apiKeys'
        

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def find_user(username = None, client_id = None):
    if username != None:
        print("searching user by username")
        try:
            userData = list(ApiKey.get(ApiKey.username == username))
            jsonData = json.dumps(model_to_dict(userData))
            return jsonData
        except: return None
    elif client_id != None:
        print("searching user by client_id")
        try:
            userData = ApiKey.select().where(ApiKey.client_id == client_id).get()
            jsonData = json.dumps(model_to_dict(userData))
            return jsonData
        except:
            return None
    else: 
        return None


           
def create_user(username: str, password: str):
    user_obj = ApiKey(
        client_id = client_id,
        client_secret = get_random_string(30),
        username = username,
        password = password
    )
    
    user_obj.save()
    return user_obj

def generate_jwt(client_id:str, client_secret:str):
    userData = find_user(None, client_id)
    print(userData)
    if userData !=None:
        user_dict = json.loads(userData)
        if client_id == user_dict['client_id'] and client_secret == user_dict['client_secret']:
            encoded_jwt = jwt.encode({"username": user_dict['username'], "client_id": user_dict['client_id'],"timeStamp": getTime()}, "secret", algorithm="HS256")
            return encoded_jwt
    else: 
        return {"code": "401", "message" : "Invalid clientId or secret!"}
    
from fastapi import APIRouter, Header, Form
from models.token import create_user, generate_jwt
from pydantic import BaseModel
from typing import Union
from typing_extensions import Annotated
import yaml
import base64

with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

secret = config['jwt']['secret']
algorithm = config['jwt']['algorithm']


routerJwt = APIRouter(
    prefix= "/v1/jwt",
    tags=["JWT token"]
)

class userRequest(BaseModel):
    username: str
    password: str
class userResponse(BaseModel):
    id: int
    username: str
    password: str
    client_id: str
    client_secret: str

@routerJwt.post("/createUser", summary="creates a user for JWT validation", response_model= userResponse)
def user(user: userRequest):
    userDict= user.model_dump()
    return create_user(userDict['username'], userDict['password'])


@routerJwt.post("/token", summary="generates JWT token for user")
def get_token(grant_type: Annotated[str, Form()], Authorization: Annotated[str, Header()]):
    Authtoken = Authorization.replace("Basic ", '')
    decoded_bytes = base64.b64decode(Authtoken)
    decoded_auth = decoded_bytes.decode("utf-8")
    clientId = decoded_auth[0:30]
    clientSecret = decoded_auth[31:]
    token = generate_jwt(clientId, clientSecret)
    return  token
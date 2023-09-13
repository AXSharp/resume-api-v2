from fastapi import APIRouter, Header, Form, Depends
from models.token import create_user, generate_jwt, validateJwt
from pydantic import BaseModel
from typing import Union
from globals import logger, raiseError
from fastapi.security import OAuth2PasswordBearer
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
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://192.168.8.51:8095/v1/jwt/token")

class userRequest(BaseModel):
    username: str
class userResponse(BaseModel):
    id: int
    username: str
    client_id: str
    client_secret: str

@routerJwt.post("/createUser", summary="creates a user for JWT validation", response_model= userResponse)
def user(user: userRequest, Authorization: Annotated[str, Depends(oauth2_scheme)]):
    token = validateJwt(Authorization)
    if token == "adm":
        userDict= user.model_dump()
        logger("INFO", "Creating a new user with username: " + userDict['username'] )
        return create_user(userDict['username'])
    else: raiseError(401, "Not an admin user!")

@routerJwt.post("/token", summary="generates JWT token for user")
def get_token(grant_type: Annotated[str, Form()], Authorization: Annotated[str, Header()]):
    logger("INFO", "grant_type: " + grant_type)
    if grant_type == "password" or grant_type == "client_credentials":
        Authtoken = Authorization.replace("Basic ", '')
        decoded_bytes = base64.b64decode(Authtoken)
        decoded_auth = decoded_bytes.decode("utf-8")
        clientId = decoded_auth[0:30]
        clientSecret = decoded_auth[31:]
        token = generate_jwt(clientId, clientSecret)
        logger("INFO", str(token))
        return  token
    else: raiseError(401, "Invalid header: grant_type!")
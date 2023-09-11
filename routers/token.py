from fastapi import APIRouter
from models.token import create_user, generate_jwt
from pydantic import BaseModel
import yaml

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


@routerJwt.get("/token", summary="generates JWT token for user")
def get_token(client_id: str, client_secret:str):
    return generate_jwt(client_id, client_secret)
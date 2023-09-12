import peewee
from typing import Any, List, Union
from fastapi import APIRouter, Header, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, Field
from pydantic.utils import GetterDict
from models.comments import list_comments, create_comment , delete_comment, update_comment
from models.token import validateJwt
from typing_extensions import Annotated

routerComments = APIRouter(
    prefix= "/v1",
    tags=["comments"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://192.168.8.51:8095/v1/jwt/token")

def raiseError(code:int, message:str):
    raise HTTPException(status_code=code, detail=message)
    
class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, peewee.ModelSelect):
            return list(res)
        return res

class CommentModel(BaseModel):
    id: Union[int, None] = None
    username: str
    comment: str
    timestamp: Union[str, None] = None
    class Config: 
        orm_mode = True
        getter_dict = PeeweeGetterDict
        
class ValidResponse(BaseModel):
    code: int = Field(examples=[200])
    message: str = Field(examples=["OK"])
        
class postRequest(BaseModel):
    username: str
    comment: str
    class Config: 
        orm_mode = True
        getter_dict = PeeweeGetterDict

class putRequest(BaseModel):
    username: Union[str, None] = None
    comment: Union[str, None] = None


@routerComments.get("/comments",response_model=Union[List[CommentModel], ValidResponse ] ,summary="All comments", description= "Returns list of all comments")
async def get_comments(Authorization: Annotated[str, Depends(oauth2_scheme)]):
    token = validateJwt(Authorization)
    if token is not None:  
        validateJwt(Authorization)    
        return list_comments()
    else: raiseError(401, "Invalid authentication credentials")

@routerComments.post("/comments", response_model= ValidResponse, summary= "Post a new comment")
async def create(comment: postRequest, Authorization: Annotated[str, Depends(oauth2_scheme)]):
    token = validateJwt(Authorization)
    if token is not None:    
        commentDict = comment.model_dump()
        await create_comment(username=commentDict['username'], comment=commentDict['comment'])
        return {"code": 200, "message": "OK"}
    else: raiseError(401, "Invalid authentication credentials")
@routerComments.delete(
    "/comments/{id}", 
    summary= "Deletes comment from database", 
    response_model= ValidResponse,
    responses= {
        200: {"content" : {"code": 200, "message": "Comment deleted successfuly!"}},
        404: {"content ": {"code": 404, "message": "Comment not found!"}},
    },)
async def delete(id: int, Authorization: Annotated[str, Depends(oauth2_scheme)]):
    token = validateJwt(Authorization)
    if token is not None: 
        validateJwt(Authorization)
        del_comment = delete_comment(id)
        print(del_comment)
        if del_comment == 0:
            return raiseError(404, "Comment not found!" )
        return {"code": 200, "message": "Comment deleted successfuly!"}
    else: raiseError(401, "Invalid authentication credentials")
    
@routerComments.put("/comments/{id}", response_model= ValidResponse, summary= "Updates comment by Id field")
async def put_comment(id, payload: putRequest, Authorization: Annotated[str, Depends(oauth2_scheme)]):
    token = validateJwt(Authorization)
    if token is not None: 
        validateJwt(Authorization)
        payload_dict = payload.model_dump()
        update_comment(id, payload_dict['comment'], payload_dict['username'])
        return {"code": 200, "message": "OK"}
    else: raiseError(401, "Invalid authentication credentials")
    
import peewee
from typing import Any, List, Union
from fastapi import APIRouter, Header
from pydantic import BaseModel, Field
from pydantic.utils import GetterDict
from models.comments import list_comments, create_comment , delete_comment, update_comment
from models.token import validateJwt
from typing_extensions import Annotated

routerComments = APIRouter(
    prefix= "/v1",
    tags=["comments"]
)

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
async def get_comments(Authorization: Annotated[str, Header()]):
    try: 
        validateJwt(Authorization)    
        return list_comments()
    except:
        return {"code": "401", "message" : "Invalid clientId or secret!"}

@routerComments.post("/comments", response_model= ValidResponse, summary= "Post a new comment")
async def create(comment: postRequest):
    commentDict = comment.model_dump()
    await create_comment(username=commentDict['username'], comment=commentDict['comment'])
    return {"code": 200, "message": "OK"}

@routerComments.delete(
    "/comments/{id}", 
    summary= "Deletes comment from database", 
    response_model= ValidResponse,
    responses= {
        200: {"content" : {"code": 200, "message": "Comment deleted successfuly!"}},
        404: {"content ": {"code": 404, "message": "Comment not found!"}},
    },)
async def delete(id: int):
    del_comment = delete_comment(id)
    print(del_comment)
    if del_comment == 0:
        return {"code": 404, "message": "Comment not found!"}
    return {"code": 200, "message": "Comment deleted successfuly!"}

@routerComments.put("/comments/{id}", response_model= ValidResponse, summary= "Updates comment by Id field")
async def put_comment(id, payload: putRequest):
    payload_dict = payload.model_dump()
    update_comment(id, payload_dict['comment'], payload_dict['username'])
    return {"code": 200, "message": "OK"}

# @routerComments.post("/test", description= "endpoint for sandbox testing!")
# def playground(comment: CommentModel):
#     comment = comment.model_dump()
#     comment = comment['comment']
#     return comment
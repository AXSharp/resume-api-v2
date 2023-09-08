import peewee
from typing import Any, List, Union
from fastapi import APIRouter
from pydantic import BaseModel, Field
from pydantic.utils import GetterDict
from models.comments import list_comments, create_comment
routerComments = APIRouter(
    prefix= "/comments",
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
    class Config: 
        orm_mode = True
        getter_dict = PeeweeGetterDict
        
class postRequest(BaseModel):
    username: str
    comment: str
    class Config: 
        orm_mode = True
        getter_dict = PeeweeGetterDict

@routerComments.get("/",response_model=List[CommentModel] ,summary="All comments", description= "Returns list of all comments")
async def get_comments():
    return list_comments()

@routerComments.post("/", response_model=List[ValidResponse], summary= "Post a new comment")
async def create(comment: postRequest):
    commentDict = comment.model_dump()
    await create_comment(username=commentDict['username'], comment=commentDict['comment'])
    return [{"code": 200, "message": "OK"}]

# @routerComments.post("/test", description= "endpoint for sandbox testing!")
# def playground(comment: CommentModel):
#     comment = comment.model_dump()
#     comment = comment['comment']
#     return comment
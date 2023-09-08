import peewee
from typing import Any, List
from fastapi import APIRouter
from pydantic import BaseModel
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
    id: int
    username: str
    comment: str
    timestamp: str
    class Config: 
        orm_mode = True
        getter_dict = PeeweeGetterDict
        
class ValidResponse(BaseModel):
    code: int
    message: str
    class Config: 
        orm_mode = True
        getter_dict = PeeweeGetterDict

@routerComments.get("/",response_model=List[CommentModel] ,summary="All comments", description= "Returns list of all comments")
async def get_comments():
    return list_comments()

@routerComments.post("/", response_model=List[ValidResponse], summary= "Post a new comment")
async def create(username:str, comment:str):
    await create_comment(username=username, comment=comment)
    return [{"code": 200, "message": "OK"}]
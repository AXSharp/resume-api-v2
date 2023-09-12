from peewee import *
from .base import BaseModel
import time

class Comment(BaseModel):
    id = IntegerField()
    username = CharField(max_length=30)
    comment = TextField()
    timestamp = CharField(max_length=100)
    
    class Meta:
        db_table = 'comments'


def getTime():
    return str(time.time())[:10]

async def create_comment(username: str, comment:str):
    
    comment_obj = Comment(
        username = username,
        comment = comment,
        timestamp = getTime()
    )
    
    comment_obj.save()
    return comment_obj


def list_comments(skip: int = 0, limit: int = 100):
    return list(Comment.select().offset(skip).limit(limit))

def delete_comment (id:int):
    return Comment.delete().where(Comment.id == id).execute()

def update_comment (id: int, comment:str, username:str):
    row = Comment.get(Comment.id == id)
    if comment != None:
        row.comment = comment
    if username != None:
        row.username = username
    row.timestamp = getTime()
    row.save()
    return row
from fastapi import HTTPException

def raiseError(code:int, message:str):
    raise HTTPException(status_code=code, detail=message)
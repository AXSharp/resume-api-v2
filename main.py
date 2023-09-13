from fastapi import FastAPI
from globals import logger
from routers import comments, token
from database import *
from logging.config import dictConfig
import uvicorn

app = FastAPI(title="Resume-API", description="A set of REST endpoints for servicing resume website.", version='0.3', debug=True)
app.include_router(comments.routerComments)
app.include_router(token.routerJwt)

@app.on_event("startup")
async def startup():
    logger("INFO", "Connecting...")
    if conn.is_closed():
        conn.connect()
        logger("INFO", "Connected to mySQL database!")
        
@app.on_event("shutdown")
async def shutdown():
    logger("INFO", "Closing connection...")
    if not conn.is_closed():
        conn.close()
        logger("INFO", "Closed connection form database!")

@app.get("/")
def read_root():
    return {"code": 200, "message": "Resume API root!"}


if __name__ == "__main__":
    uvicorn.run(app, port=8000, host= '0.0.0.0')
from fastapi import FastAPI
from routers import comments
from database import *
import uvicorn


app = FastAPI(title="Resume-API", description="A set of REST endpoints for servicing resume website.", version='0.2')
app.include_router(comments.routerComments)



@app.on_event("startup")
async def startup():
    print("Connecting...")
    if conn.is_closed():
        conn.connect()
        print("Connected to mySQL database!")
        
@app.on_event("shutdown")
async def shutdown():
    print("Closing connection...")
    if not conn.is_closed():
        conn.close()
        print("Closed connection form database!")

@app.get("/")
def read_root():
    return {"code": 200, "message": "Resume API root!"}


if __name__ == "__main__":
    uvicorn.run(app, port=8000, host= '0.0.0.0')
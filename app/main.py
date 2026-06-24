# Importing the FastAPI module
from random import randrange
# from turtle import title

from fastapi import FastAPI, HTTPException, status, Response
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status Refer for HTTP Response Codes


from . import models # Importing models.py file which has information about DB Tables
from .database import engine, SessionLocal # Importing database.py file which has SqlAlchemy database connections and sessions logic

from . routers import post, user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)

# This is called as a path operation
@app.get("/") # A "path" is also commonly called an "endpoint" or a "route".
async def root(): # async needed only when time constraints are present in function calling, can remove it.
    return {"message": "Hello World"} # Here FastAPI automatically converts python dictionaries into JSON



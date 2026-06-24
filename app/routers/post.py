from .. import schemas

# Importing the FastAPI module
from random import randrange
# from turtle import title

from fastapi import FastAPI, HTTPException, status, Response, APIRouter
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status Refer for HTTP Response Codes

# Importing Body from fastapi.params to capture the body content passed in JSON format from the client side in the POST method (for example: Postman)
from fastapi.params import Body, Depends

# Getting Schema Validation file
from app import schemas
from .. schemas import Post

from typing import Optional, List

import time



from .. import models # Importing models.py file which has information about DB Tables
from .. database import engine, SessionLocal # Importing database.py file which has SqlAlchemy database connections and sessions logic
from .. database import get_db
from .. import utils

from sqlalchemy.orm import Session



router = APIRouter()

# To GET all the posts
@router.get("/posts", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):


    posts = db.query(models.Post).all() # SQLALCHEMY ORM

    return posts


# To create a post
@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse) # Creating a POST method with the path name -> /createposts , By default, sends Status Code as 201 upon successful creation.
def create_posts(posts: schemas.PostCreate, db: Session = Depends(get_db)): # Here we are doing input validation by checking if the variable posts has the title and content and are of right type by using Post Extended class
    

    new_post = models.Post(**posts.dict()) # Easier way -> Takes the Pydantic valdiation model which is in dicticonary and unpacks it.

    db.add(new_post) # Add to the DB
    db.commit() # Commit changes to the DB
    db.refresh(new_post) # Get the latest post back

    return new_post


# To get Individual post details by using ID
@router.get("/post/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):


    found_post = db.query(models.Post).filter(models.Post.id == id).first() # SQLALCHEMY ORM

    # Handling not found via HTTPException
    if not found_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=(f"{id} not found"))
    
    return found_post


# To delete a post
@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):

    found_post = db.query(models.Post).filter(models.Post.id == id) # SQLALCHEMY ORM

    # If there is no post of that ID -> Raise an exception
    if found_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=(f"{id} not found"))
    
    found_post.delete(synchronize_session=False)
    db.commit()

    # 204 Status code does not allow any content in the console as 204 signifies NO_CONTENT
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# To Update a post
@router.put("/posts/{id}", response_model=schemas.PostResponse)
def update_post(id: int, new_post:schemas.PostCreate, db: Session = Depends(get_db)): # Validating the input Post class Schema


    updated_post = db.query(models.Post).filter(models.Post.id == id) # SQLALCHEMY ORM

    if updated_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=(f"{id} not found"))
    
    # updated_post.update({'title':"my new title", 'content':"my new content"}, synchronize_session=False)
    updated_post.update(new_post.dict(), synchronize_session=False)
    db.commit()

    return updated_post.first()

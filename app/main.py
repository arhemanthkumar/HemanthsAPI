# Importing the FastAPI module
from random import randrange
# from turtle import title

from fastapi import FastAPI, HTTPException, status, Response
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status Refer for HTTP Response Codes

# Importing Body from fastapi.params to capture the body content passed in JSON format from the client side in the POST method (for example: Postman)
from fastapi.params import Body, Depends

# Getting Schema Validation file
from app import schemas
from .schemas import Post

from typing import Optional, List

import time



import psycopg # Adapter for PostgresSQL
from psycopg.rows import dict_row
# Need dict_row to get column names when a query result comes

from . import models # Importing models.py file which has information about DB Tables
from .database import engine, SessionLocal # Importing database.py file which has SqlAlchemy database connections and sessions logic
from .database import get_db
from . import utils

from sqlalchemy.orm import Session

# while True:
#     try:
#         conn = psycopg.connect(
#             host = 'localhost',
#             dbname = 'fastapi',
#             user = "postgres",
#             password = "20032003",
#             row_factory = dict_row
#         )

#         cursor = conn.cursor()
#         print("Database Connection Successful")
#         break # Coming out of While Loop

#     except Exception as error:
#         print("Connection to the Database failed")
#         print("Error:", error)
#         print()
#         time.sleep(5)
#         continue
        

models.Base.metadata.create_all(bind=engine)

# We are creating an (object - app) instance of a class called FastAPI
# This will be the main point of interaction to create all the APIs
app = FastAPI()




# Example of the storage to do CRUD based operations.
# my_posts = [
#     {
#         "title": "Example title 1",
#         "content": "Example content 1",
#         "id": 1
#     },
#     {
#         "title": "Favourite Foods",
#         "content": "I like Pizza",
#         "id": 2
#     }
# ]

# To check if my_posts DB (list) has a post by the ID.
# def find_post(id):
#     for individual_post in my_posts:
#         if individual_post["id"] == id:
#             return individual_post
        
# To get index of a post in my_posts DB (list)
# def find_index(id):
#     for index, post in enumerate(my_posts):
#         if post["id"] == id:
#             return index

# This is called as a path operation
@app.get("/") # A "path" is also commonly called an "endpoint" or a "route".
async def root(): # async needed only when time constraints are present in function calling, can remove it.
    return {"message": "Hello World"} # Here FastAPI automatically converts python dictionaries into JSON

'''
To summarize this:
get -> Method name
"/" -> Path name
root() -> Function name
'''

# Test path operation for SQLAlchemy
# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):
#     all_posts = db.query(models.Post).all()
#     return all_posts


# To GET all the posts
@app.get("/posts", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):

    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()

    posts = db.query(models.Post).all() # SQLALCHEMY ORM

    return posts

# @app.post("/createposts") # Creating a POST method with the path name -> /createposts
# def create_posts(payLoad: dict = Body(...)): # This captures the Body content passed in JSON in dictionary format in the payLoad variable
#     print(payLoad) # Printing to check the contents
#     return {"Success": f"Your Title: {payLoad['title']} and Your Content: {payLoad['content']}"} # Return message


# To create a post
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse) # Creating a POST method with the path name -> /createposts , By default, sends Status Code as 201 upon successful creation.
def create_posts(posts: schemas.PostCreate, db: Session = Depends(get_db)): # Here we are doing input validation by checking if the variable posts has the title and content and are of right type by using Post Extended class
    
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",(posts.title, posts.content, posts.published) )
    # new_post = cursor.fetchone()
    # conn.commit()

    # new_post = models.Post(title=posts.title, content=posts.content, published=posts.published) # SQLALCHEMY ORM
    new_post = models.Post(**posts.dict()) # Easier way -> Takes the Pydantic valdiation model which is in dicticonary and unpacks it.

    db.add(new_post) # Add to the DB
    db.commit() # Commit changes to the DB
    db.refresh(new_post) # Get the latest post back

    return new_post


# To get Individual post details by using ID
@app.get("/post/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    # found_post = find_post(id)

    # cursor.execute(f""" SELECT * FROM posts WHERE id = {id} """)
    # found_post = cursor.fetchall()

    found_post = db.query(models.Post).filter(models.Post.id == id).first() # SQLALCHEMY ORM

    # Handling not found via HTTPException
    if not found_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=(f"{id} not found"))
    
    return found_post


# To delete a post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):

    # Check the index with the ID
    # found_index = find_index(id)

    # cursor.execute(f""" DELETE FROM posts WHERE id = {id} RETURNING *; """)
    # found_post = cursor.fetchone()
    # conn.commit()

    found_post = db.query(models.Post).filter(models.Post.id == id) # SQLALCHEMY ORM

    # If there is no post of that ID -> Raise an exception
    if found_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=(f"{id} not found"))
    
    found_post.delete(synchronize_session=False)
    db.commit()

    # 204 Status code does not allow any content in the console as 204 signifies NO_CONTENT
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# To Update a post
@app.put("/posts/{id}", response_model=schemas.PostResponse)
def update_post(id: int, new_post:schemas.PostCreate, db: Session = Depends(get_db)): # Validating the input Post class Schema

    # cursor.execute(f""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = {id} RETURNING *; """,(new_post.title, new_post.content, new_post.published))
    # updated_post = cursor.fetchone()
    # conn.commit()

    updated_post = db.query(models.Post).filter(models.Post.id == id) # SQLALCHEMY ORM

    if updated_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=(f"{id} not found"))
    
    # updated_post.update({'title':"my new title", 'content':"my new content"}, synchronize_session=False)
    updated_post.update(new_post.dict(), synchronize_session=False)
    db.commit()

    return updated_post.first()

# To create a user
@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse) 
def create_posts(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # hash the password from user.password
    hashed_password = utils.hash(user.password)

    user.password = hashed_password

    new_user = models.User(**user.dict()) 

    db.add(new_user) # Add to the DB
    db.commit() # Commit changes to the DB
    db.refresh(new_user) # Get the latest post back

    return new_user

# To get ID of a user
@app.get("/users/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db:Session = Depends(get_db)):

    found_user = db.query(models.User).filter(models.User.id == id).first()

    if not found_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"User with id {id} does not exist")
    
    return found_user
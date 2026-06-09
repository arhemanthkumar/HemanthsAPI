# Importing the FastAPI module
from random import randrange

from fastapi import FastAPI, HTTPException, status, Response
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status Refer for HTTP Response Codes

# Importing Body from fastapi.params to capture the body content passed in JSON format from the client side in the POST method (for example: Postman)
from fastapi.params import Body

from pydantic import BaseModel # For input schema validation
# Pydantic has lot of inbuilt data types which we can use to validate
# https://pydantic.dev/docs/validation/1.10/usage/types/

from typing import Optional

import time

import psycopg # Adapter for PostgresSQL
from psycopg.rows import dict_row
# Need dict_row to get column names when a query result comes

while True:
    try:
        conn = psycopg.connect(
            host = 'localhost',
            dbname = 'fastapi',
            user = "postgres",
            password = "20032002",
        row_factory = dict_row
        )

        cursor = conn.cursor()
        print("Database Connection Successful")
        break # Coming out of While Loop

    except Exception as error:
        print("Connection to the Database failed")
        print("Error:", error)
        print()
        time.sleep(5)
        

# We are creating an (object - app) instance of a class called FastAPI
# This will be the main point of interaction to create all the APIs
app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True # Keeping True as default value

# Example of the storage to do CRUD based operations.
my_posts = [
    {
        "title": "Example title 1",
        "content": "Example content 1",
        "id": 1
    },
    {
        "title": "Favourite Foods",
        "content": "I like Pizza",
        "id": 2
    }
]

# To check if my_posts DB (list) has a post by the ID.
def find_post(id):
    for individual_post in my_posts:
        if individual_post["id"] == id:
            return individual_post
        
# To get index of a post in my_posts DB (list)
def find_index(id):
    for index, post in enumerate(my_posts):
        if post["id"] == id:
            return index

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

# Test path operation
@app.get("/posts")
def get_posts():
    return {"data": my_posts}

# @app.post("/createposts") # Creating a POST method with the path name -> /createposts
# def create_posts(payLoad: dict = Body(...)): # This captures the Body content passed in JSON in dictionary format in the payLoad variable
#     print(payLoad) # Printing to check the contents
#     return {"Success": f"Your Title: {payLoad['title']} and Your Content: {payLoad['content']}"} # Return message


@app.post("/posts", status_code=status.HTTP_201_CREATED) # Creating a POST method with the path name -> /createposts , By default, sends Status Code as 201 upon successful creation.
def create_posts(posts: Post): # Here we are doing input validation by checking if the variable posts has the title and content and are of right type by using Post Extended class
    # print(posts) # Printing to check the contents
    post_dict = posts.dict()
    post_dict["id"] = randrange(0, 1000000)
    my_posts.append(post_dict)
    # return {"Success"} # Return message
    # print(posts.dict())
    return post_dict

# To get Individual post details by using ID
@app.get("/post/{id}")
def get_post(id: int):
    found_post = find_post(id)

    # Handling not found via HTTPException
    if not found_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=(f"{id} not found"))
    
    return found_post

# To delete a post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):

    # Check the index with the ID
    found_index = find_index(id)

    # If there is no post of that ID -> Raise an exception
    if found_index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=(f"{id} not found"))

    # ID of the post must be present, we have the index, using that index, pop the post from my_posts
    my_posts.pop(found_index)
    
    # 204 Status code does not allow any content in the console as 204 signifies NO_CONTENT
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# To Update a post
@app.put("/posts/{id}")
def update_post(id: int, new_post:Post): # Validating the input Post class Schema

    # Check the index with the ID
    found_index = find_index(id)

    # If there is no post of that ID -> Raise an exception
    if found_index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=(f"{id} not found"))
    
    # As the new_post is not in dict format, we need to convert it into dict
    new_post_dict = new_post.dict()

    # now the new_post_dict does not have a ID, so we add the ID that is passed which is validated and present in our my_posts DB
    new_post_dict["id"] = id

    # Finally we replace the index of the my_posts with our newly constructed dict
    my_posts[found_index] = new_post_dict
    
    return new_post
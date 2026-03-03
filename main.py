# Importing the FastAPI module
from fastapi import FastAPI

from fastapi.params import Body

# We are creating an (object - app) instance of a class called FastAPI
# This will be the main point of interaction to create all the APIs
app = FastAPI()


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
    return {"data": "This is your posts"}

@app.post("/createposts") # Creating a POST method witht the path name -> /createposts
def create_posts(payLoad: dict = Body(...)): # This captures the Body content passed in JSON in dictionary format in the payLoad variable
    print(payLoad) # Printing to check the contents
    return {"messsage": "Successfully created posts"} # Return message
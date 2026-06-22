from pydantic import BaseModel, ConfigDict, EmailStr # For input schema validation
# Pydantic has lot of inbuilt data types which we can use to validate
# https://pydantic.dev/docs/validation/1.10/usage/types/

from datetime import datetime



# SCHEMA from Pydantic Model
class Post(BaseModel):
    title: str
    content: str
    published: bool = True # Keeping True as default 
    

class PostCreate(Post):
    pass

class PostResponse(Post): # For validation of responses which are sent back to the user.
    # title: str
    # content: str
    # published: bool # These can be avoided as it is inheriting the Post Class which is Base Model
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
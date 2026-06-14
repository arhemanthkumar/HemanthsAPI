from pydantic import BaseModel

# SCHEMA from Pydantic Model
class Post(BaseModel):
    title: str
    content: str
    published: bool = True # Keeping True as default value
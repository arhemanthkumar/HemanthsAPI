from .. import schemas

from fastapi import FastAPI, HTTPException, status, Response, APIRouter
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status Refer for HTTP Response Codes

# Importing Body from fastapi.params to capture the body content passed in JSON format from the client side in the POST method (for example: Postman)
from fastapi.params import Body, Depends

# Getting Schema Validation file
from app import schemas
from .. schemas import Post

from .. import models # Importing models.py file which has information about DB Tables
from .. database import engine, SessionLocal # Importing database.py file which has SqlAlchemy database connections and sessions logic
from .. database import get_db
from .. import utils

from sqlalchemy.orm import Session

router = APIRouter(
    tags=['Users']
)

# To create a user
@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse) 
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
@router.get("/users/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db:Session = Depends(get_db)):

    found_user = db.query(models.User).filter(models.User.id == id).first()

    if not found_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"User with id {id} does not exist")
    
    return found_user
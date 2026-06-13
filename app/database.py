from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select

from sqlalchemy.orm import DeclarativeBase

# SQLALCHEMY_DATABASE_URL = "postgresql:<username>:<password>@<ip-address/hostname>/<database_name>"
SQLALCHEMY_DATABASE_URL = "postgresql+pyscopg:postgres:20032003@localhost/fastapi"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

sessionLocal = Session(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass

# Fom FastAPI SQLAlchemy docs.
# class Hero(SQLModel, table=True):
#     id: int | None = Field(default=None, primary_key=True)
#     name: str = Field(index=True)
#     age: int | None = Field(default=None, index=True)
#     secret_name: str


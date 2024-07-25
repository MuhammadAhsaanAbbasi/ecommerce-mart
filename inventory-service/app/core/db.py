from app.setting import DATABASE_URL
from sqlmodel import SQLModel, create_engine, Session
from typing import Annotated
from fastapi import Depends
import os

connectionstring = str(DATABASE_URL).replace(
    "postgresql", "postgresql+psycopg2"
) 

engine = create_engine(connectionstring, connect_args={"sslmode" : "require"}, pool_recycle=600, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session 

DB_SESSION = Annotated[Session, Depends(get_session)]
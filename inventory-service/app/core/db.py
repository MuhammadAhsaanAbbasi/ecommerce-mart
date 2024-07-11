from app.setting import DATABASE_URL
from sqlmodel import SQLModel, create_engine, Session
from typing import Annotated
from fastapi import Depends
import os

connection_string = os.getenv('DATABASE_URL')
engine = create_engine(str(connection_string), connect_args={"sslmode": "require"} )

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

DB_SESSION = Annotated[Session, Depends(get_session)]
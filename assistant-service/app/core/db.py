from app import setting
from sqlmodel import SQLModel, create_engine, Session
from typing import Annotated
from fastapi import Depends

connectionstring = str(setting.DATABASE_URL).replace(
    "postgresql", "postgresql+psycopg2"
)

engine = create_engine(connectionstring, connect_args={"sslmode" : "require"}, pool_recycle=600, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

DB_SESSION = Annotated[Session, Depends(get_session)]
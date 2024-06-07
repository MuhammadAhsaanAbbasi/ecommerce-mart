from sqlmodel import SQLModel, Field,Relationship
from typing import Optional
import datetime
from pydantic import BaseModel, EmailStr
from .base import BaseIdModel
import requests

# University BaseModel class
class UniversityBase(SQLModel):
    university_name: str = Field(index=True)
    university_desc: Optional[str] = Field(default=None)

# University Model and Relationship Table
class University(UniversityBase, BaseIdModel, table=True):
    """
    Fields:
    university_name, university_desc (required): inherited from UniversityBase
    """
    university_logo_url: Optional[str] = Field(default=None)
    # programs: list["Program"] = Relationship(back_populates="university")
    admin_id: Optional[int] = Field(default=None, foreign_key="admin.id")
    admins: "Admin" = Relationship(back_populates="university")

# University Update Class
class UniversityUpdate(SQLModel):
    university_name: str | None = None
    university_desc: str | None = None

# Program BaseModel class
class ProgramBase(SQLModel):
    program_name: str
    program_desc: str | None = None

# Program Model and Relationship Table
class Program(ProgramBase, BaseIdModel, table=True):
    """
    Fields:
    program_name, program_desc (required): inherited from ProgramBase
    """
    university_id: Optional[int] = Field(default=None, foreign_key="university.id")
    # university: University = Relationship(back_populates="programs")
    courses: list["Course"] = Relationship(back_populates="program")

# Program Update Class
class ProgramUpdate(SQLModel):
    program_name: str | None = None
    program_desc: str | None = None

# Course BaseModel class
class CourseBase(SQLModel):
    course_name: str
    course_desc: str | None = None
    course_duration: str | None = None

class CourseUserLink(SQLModel, table=True):
    course_id: Optional[int] = Field(default=None, foreign_key="course.id", primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="users.id", primary_key=True)

# Course Model and RelationShip Table
class Course(CourseBase, BaseIdModel, table=True):
    """
    Fields:
    course_name, course_desc (required): inherited from CourseBase
    """
    # 4. Course Relationship with Program
    program_id: Optional[int] = Field(default=None, foreign_key="program.id")
    program: Program = Relationship(back_populates="courses")
    
    # 5. Course Relationship with User (Student & Instructor)
    users: Optional[list["Users"]] = Relationship(back_populates="courses", link_model=CourseUserLink)

# Course Updated
class CourseUpdate(SQLModel):
    """
    Fields:
    course_name (optional): str: Name of the Course
    course_desc (optional): str: Description of the Course
    """
    course_name: str | None = None
    course_desc: str | None = None
    course_duration: str | None = None

class UserBase(SQLModel):
    username: str = Field(index=True)
    email: str = Field(index=True)
    hashed_password: Optional[str] = Field(default=None, index=True)
    imageUrl: Optional[str] = Field(default=None)
    is_active: bool = Field(default=True)
    is_verified: bool = Field(default=False)
    otp: Optional[str] = Field(default=None, index=True)

# Users Model
class Users(UserBase, BaseIdModel, table=True):
    role: str = Field(default="user")
    # 6. Relationship with Course
    courses: Optional[list["Course"]] = Relationship(back_populates="users", link_model=CourseUserLink)
    
    #7. Relationship with Admin

# Admin Model
class Admin(UserBase, BaseIdModel, table=True):
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    university: Optional[list["University"]] = Relationship(back_populates="admins")

# class Secretkey(SQLModel, table=True):
#     key: str = Field()

class Token(SQLModel):
    access_token: str
    token_type: str
    access_expires_in: int
    refresh_token: str
    refresh_token_expires_in: int

class TokenData(BaseModel):
    username: str | None = None
    email: str | None = None
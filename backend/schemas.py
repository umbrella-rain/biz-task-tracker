from models import UserRole
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from models import TaskStatus

class ClientSchema(BaseModel):
    email: EmailStr # get customer email
    name: str = Field(min_length = 2, max_length = 50) # get customer name
    description: str | None = Field(max_length = 250) # get customer bio
    phone_number: str | None = Field(default = "123123") # get customer phone number
    gender: str | None = Field(default = "Female") # get customer gender
    age: int = Field(ge = 14) # get customer age
    status: str | None # current status of the customer
    priority: int = Field(default = 1, ge=1, le=3) # 1 is pending, 2 is default, 3 is high priority

    class Config:
        from_attributes = True


class ClientRead(ClientSchema):
    id: str

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    description: Optional[str] = None
    phone_number: Optional[str] = None
    gender: Optional[str] = None
    age: Optional[int] = None
    status: Optional[str] = None
    priority: Optional[int] = None

    class Config:
        from_attributes = True



class TaskSchema(BaseModel):
    client_id: str
    title: str = Field(min_length = 2, max_length = 50)
    status: str | None
    description: str = Field(min_length = 2, max_length = 250)

    class Config:
        from_attributes = True

class UserRead (BaseModel):
    id: str
    email: EmailStr
    role: UserRole

    class Config:
        from_attributes = True


class TaskRead(TaskSchema):
    id: str
    creator_id: str
    status: str
    creator: Optional[UserRead] = None

    class Config:
        from_attributes = True

class TaskUpdate(BaseModel):
    title: str = Field(min_length = 2, max_length = 50)
    status: Optional[TaskStatus] = None
    description: str = Field(min_length = 2, max_length = 250)

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: UserRole


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

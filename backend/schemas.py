from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class UserSchema(BaseModel):
    email: EmailStr # get customer email
    name: str = Field(min_length = 2, max_length = 50) # get customer name
    description: str | None = Field(max_length = 250) # get customer bio
    phone_number: str | None = Field(default = 123123)
    gender: str | None = Field(default = "Female") # get customer gender
    age: int = Field(ge = 14) # get customer age
    status: str | None # current status of the customer
    priority: int = Field(default = 1, ge=1, le=3) # 1 is pending, 2 is default, 3 is high priority

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
    title: str = Field(min_length = 2, max_length = 50)
    status: str | None
    description: str = Field(min_length = 2, max_length = 250)

    class Config:
        from_attributes = True


class TaskRead(TaskSchema):
    id: str
    creator_id: str
    status: str

    class Config:
        from_attributes = True



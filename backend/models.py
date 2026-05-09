import enum
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from database import Base


class TaskStatus(str, enum.Enum):
    NEW = 'new'
    DONE = 'done'



class Task(Base):
    __tablename__ = 'tasks'
    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(Enum(TaskStatus), nullable=False)

    creator_id = Column(String, ForeignKey('users.id'))
    creator = relationship('User', back_populates='tasks')






class User(Base):
    __tablename__ = 'users'
    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    name = Column(String)
    description = Column(String)
    phone_number = Column(String, nullable=True)
    gender = Column(String)
    age = Column(Integer)
    status = Column(String)
    priority = Column(Integer)
    tasks = relationship('Task', back_populates='creator')
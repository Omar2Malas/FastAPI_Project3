# This file defines the database model for the ToDo application. 
from database import Base
from sqlalchemy import Column, Integer, String, Boolean

class Todos(Base): # this class inherits from Base so SQLAlchemy knows that this class is a database table
    __tablename__ = 'todos'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
# This file defines the database model for the ToDo application. 
from database import Base
from sqlalchemy import Column, Integer, String, Boolean , ForeignKey

class Users(Base): 
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True) 
    email = Column(String , unique = True )
    username = Column(String , unique = True )
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String )
    is_active = Column(Boolean, default=True)
    role = Column(String)

    
class Todos(Base): # this class inherits from Base so SQLAlchemy knows that this class is a database table
    __tablename__ = 'todos'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    owner_id = Column(Integer , ForeignKey('users.id'))

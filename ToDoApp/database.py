# This code sets up the database connection and configuration for a ToDo application using SQLAlchemy. 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = 'sqlite:///./todos.db' # SQLite database URL used to connect to the database. The database file will be created in the current directory with the name 'todo.db'. The 'sqlite:///' prefix indicates that we are using SQLite as our database engine.

engine = create_engine(SQLALCHEMY_DATABASE_URL,connect_args={'check_same_thread':False}) # the engine is used to connect the python code to the database and execute SQL statements, the connect_args={'check_same_thread':False} is used to allow multiple threads to access the database connection .

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # Creates a SQLAlchemy session factory using the 'sessionmaker' function. The 'autocommit' parameter is set to False to disable automatic commits, and the 'autoflush' parameter is set to False to prevent automatic flushing of changes to the database. The 'bind' parameter is set to the previously created engine, which allows the session to connect to the database.

Base=declarative_base() # Creates a base class for declarative class definitions using the 'declarative_base' function. This base class will be used to define the database models (tables) in the application. By inheriting from this base class, we can create classes that represent database tables and their relationships.
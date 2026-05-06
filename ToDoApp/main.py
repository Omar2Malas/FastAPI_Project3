from fastapi import FastAPI,Depends
from typing import Annotated
import models
from models import Todos
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)  # This line creates the database tables based on the models defined in the 'models' module.

def get_db(): # This function is a dependency that provides a database session to the endpoint functions
    db = SessionLocal()  # create the session object to interact with the database
    try: 
        yield db # yield the database session to the endpoint functions that will use it
    finally:
        db.close()  

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/")
async def read_all(db: db_dependency ): # dependency injection is used to provide the database session to the endpoint function
    return db.query(Todos).all()  
# annotated type is used to specify that the 'db' parameter is of type 'Session' and that it depends on the 'get_db' function 



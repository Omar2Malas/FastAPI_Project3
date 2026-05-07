from fastapi import FastAPI,Depends,HTTPException, status , Path
from typing import Annotated

from pydantic import BaseModel, Field
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

class ToDoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete : bool


@app.get("/",status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency ): # dependency injection is used to provide the database session to the endpoint function
    return db.query(Todos).all()  
# annotated type is used to specify that the 'db' parameter is of type 'Session' and that it depends on the 'get_db' function 
# what is query : The 'query' method is used to create a query object that allows you to retrieve data from the database.

@app.get("/todo/{todo_id}",status_code=status.HTTP_200_OK)
async def read_todo(db:db_dependency,todo_id:int = Path(gt = 0 )): 
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first() 
    # .first() is used to retrieve the first result of the query, which in this case will be the ToDo item with the specified 'todo_id'
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo_model

@app.post("/todo",status_code=status.HTTP_201_CREATED)
def create_todo(db:db_dependency,todo_request:ToDoRequest):
    todo_model = Todos(**todo_request.model_dump()) # create a new instance of the 'Todos' model, which represents a ToDo item in the database

    db.add(todo_model)
    db.commit()

@app.put("/todo/{todo_id}",status_code=status.HTTP_200_OK)
async def update_todo(db:db_dependency, 
                      todo_id:int = Path(gt = 0),
                      todo_request:ToDoRequest = None):
     
    # todorequest:ToDoRequest = None is used to specify that the 'todo_request' parameter is optional and can be None if not provided in the request body
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete
    
    db.add(todo_model)
    db.commit()

@app.delete("/todo/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db:db_dependency, todo_id:int = Path(gt = 0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    db.delete(todo_model)
    db.commit()
    
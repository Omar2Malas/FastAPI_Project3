from fastapi import FastAPI
import models
from database import engine
from routers import auth , todos   

app = FastAPI()

models.Base.metadata.create_all(bind=engine)  # This line creates the database tables based on the models defined in the 'models' module.

app.include_router( auth.router)
app.include_router( todos.router)



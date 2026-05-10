from typing_extensions import Annotated
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from database import SessionLocal
from models import Users
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette import status

router = APIRouter()

bcrypt_context = CryptContext(schemes = ['bcrypt'], deprecated = 'auto')

class CreateUserRequest(BaseModel):
    email: str
    username: str
    first_name: str
    last_name: str
    password: str
    role: str

def get_db(): # This function is a dependency that provides a database session to the endpoint functions
    db = SessionLocal()  # create the session object to interact with the database
    try: 
        yield db # yield the database session to the endpoint functions that will use it
    finally:
        db.close()  

db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/auth",status_code=status.HTTP_201_CREATED)
async def create_user(create_user_request: CreateUserRequest , db: db_dependency):
    create_user_model = Users(
         email=create_user_request.email,
         username=create_user_request.username,
         first_name=create_user_request.first_name,
         last_name=create_user_request.last_name,
         role = create_user_request.role,
         hashed_password = bcrypt_context.hash(create_user_request.password),
         is_active = True
    )
    db.add(create_user_model) # when database added
    db.commit() # commit the transaction to save the changes to the database
from datetime import datetime, timedelta, timezone
from typing_extensions import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from database import SessionLocal
from models import Users
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm , OAuth2PasswordBearer
from jose import jwt
from dotenv import load_dotenv
import os

load_dotenv()

router = APIRouter()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')


bcrypt_context = CryptContext(schemes = ['bcrypt'], deprecated = 'auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='token') 

class CreateUserRequest(BaseModel):
    email: str
    username: str
    first_name: str
    last_name: str
    password: str
    role: str

class Token(BaseModel):
    access_token: str
    token_type: str

def get_db(): # This function is a dependency that provides a database session to the endpoint functions
    db = SessionLocal()  # create the session object to interact with the database
    try: 
        yield db # yield the database session to the endpoint functions that will use it
    finally:
        db.close()  

db_dependency = Annotated[Session, Depends(get_db)]

def authenticate_user(db: Session, username: str, password: str): 
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False 
    return user

def create_access_token(username : str , user_id = int , expires_delta = timedelta): # This function creates a JWT access token for the authenticated user
    encode = {"sub":username , "id":user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp":expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/auth",status_code=status.HTTP_201_CREATED) # This endpoint is used to create a new user in the database 
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

@router.post("/token",response_model=Token) # This endpoint is used to authenticate a user and generate an access token for them
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        return "Failed authenticatication"
    token = create_access_token(user.username, user.id, timedelta(minutes=20))
    return {"access_token": token, "token_type": "bearer"} # The response includes the generated access token and the token type (bearer) that indicates how the token should be used in subsequent requests to protected endpoints.



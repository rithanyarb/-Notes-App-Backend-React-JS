from datetime import timedelta, timezone, datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status
from database import SessionLocal
from models import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY = "e509e89f4150b105bb4827f5c14ff3f40db71679ab8198657be060d867efc00b"
ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

class CreateUserDetails(BaseModel):
    user_name: str = Field(min_length=5)
    email: str = Field(min_length=3)
    password: str
    is_active: bool

class Token(BaseModel):
    access_token: str
    token_type: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.user_name == username).first()
    if not user or not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_name: str = payload.get('sub')
        user_id: int = payload.get('id')
        if user_name is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Could not validate user.")
        return {'user_name': user_name, 'user_id': user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate user.")

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_details: CreateUserDetails):
    user = db.query(Users).filter(
        (Users.user_name == create_user_details.user_name) | (Users.email == create_user_details.email)
    ).first()
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Username or email already exists")
    create_user_model = Users(
        user_name=create_user_details.user_name,
        email=create_user_details.email,
        hashed_password=bcrypt_context.hash(create_user_details.password),
        is_active=create_user_details.is_active
    )
    db.add(create_user_model)
    db.commit()

@router.post("/token/", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate user.")
    token = create_access_token(user.user_name, user.user_id, timedelta(minutes=20))
    return {'access_token': token, 'token_type': 'bearer'}
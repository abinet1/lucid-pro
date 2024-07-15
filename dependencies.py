from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session
import jwt
import models
from database import SessionLocal
from passlib.context import CryptContext
from typing import Annotated
import os

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db: Annotated[Session, Depends(get_db)], email: str) -> models.User:
    user_not_found = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Could not find the user",
        headers={"WWW-Authenticate": "Bearer"},
    )
    db_user = db.query(models.User).filter(models.User.email == email).first()
    if db_user is None:
        raise user_not_found
    
    return db_user

def authenticate_user(db: Annotated[Session, Depends(get_db)], email: str, password: str):
    user = get_user(db, email)
    if not user:
        return False
    
    if not verify_password(password, user.password):
        return False
    
    return user

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db) ):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        
        user = get_user(db, email=email)

        if user is None:
            raise credentials_exception
        return user

    except InvalidTokenError:
        raise credentials_exception
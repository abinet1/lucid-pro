from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated, List
import models
import schemas
import dependencies
from datetime import datetime

router = APIRouter()

@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    user_credential: schemas.UserBase, db: Session = Depends(dependencies.get_db)
):
    user = dependencies.authenticate_user(db, user_credential.email, user_credential.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = dependencies.create_access_token(
        data={"sub": user.email}
    )
    return schemas.Token(access_token=access_token, token_type="bearer")

@router.post("/signup", response_model=schemas.TokenData)
async def signup_user(user: schemas.UserBase, db: Annotated[Session, Depends(dependencies.get_db)]):

    hashed_password = dependencies.get_password_hash(user.password)
    db_user = models.User(email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    access_token = dependencies.create_access_token(data={"sub": db_user.email})
    return {'id': db_user.id, 'email': db_user.email, "access_token": access_token, "token_type": "bearer"}

@router.get("/users/me/", response_model=schemas.User)
async def read_users_me(
    current_user: Annotated[schemas.UserBase, Depends(dependencies.get_current_user)],
):
    return current_user

@router.post("/posts/", response_model=schemas.PostBase)
async def create_post(post: schemas.Post, user: Annotated[schemas.UserBase, Depends(dependencies.get_current_user)], db: Annotated[Session, Depends(dependencies.get_db)]):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_post = models.Post(**post.model_dump(), user_id=user.id, date=str(datetime.now()))
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@router.get("/posts/", response_model=List[schemas.PostBase])
async def read_posts(user: Annotated[schemas.UserBase, Depends(dependencies.get_current_user)], db: Annotated[Session, Depends(dependencies.get_db)], skip: int = 0, limit: int = 10):
    
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
     
    posts = db.query(models.Post).filter(models.Post.user_id == db_user.id).offset(skip).limit(limit).all()
    return posts

@router.delete("/posts/{id}", response_model=schemas.PostBase)
async def delete_posts(id: int, user: Annotated[schemas.UserBase, Depends(dependencies.get_current_user)], db: Annotated[Session, Depends(dependencies.get_db)]):
    posts = db.query(models.Post).get(id)
    if posts is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not Find the post",
            headers={"WWW-Authenticate": "Bearer"},
        )
    db.delete(posts)
    db.commit()
    return posts

@router.get("/posts/{id}", response_model=schemas.PostBase)
async def read_post(id: int, user: Annotated[schemas.UserBase, Depends(dependencies.get_current_user)], db: Annotated[Session, Depends(dependencies.get_db)]):

    posts = db.query(models.Post).get(id)
    if posts is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not Find the post",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return posts
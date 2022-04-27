from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import models, schemas

from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from typing import Optional

SECRET_KEY = "17ff87d2d54043a933c9cf8fd8f221010a956d16a3e8f4bf902ea66ebc76d62f"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 10

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Users functions
## C: Create users
def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password, created_at=datetime.now())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

## R: Read users
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).filter(models.User.discarded_at == None).offset(skip).limit(limit).all()

## U: Update users
def update_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()

## D: Delete users
def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db_user.discarded_at = datetime.now()
    db.commit()
    db.refresh(db_user)
    return db_user


# Items functions
## C: Create items
def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id, created_at=datetime.now())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

## R: Read items
def get_item(db: Session, item_id: int):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
        
    return db_item

def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()

def get_items_by_users(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Item).filter(models.Item.owner_id == user_id).offset(skip).limit(limit).all()

## U: Update item
def update_item(db: Session, item_id: int, title: str, description: str, owner_id: int):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    else:
        db_item.title = title
        db_item.description = description
        db_item.owner_id = owner_id
        db_item.updated_at = datetime.now()
        db.commit()
        db.refresh(db_item)
    return db_item

## D: Delete items
def delete_item(db: Session, item_id: int):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    else:    
        db_item.discarded_at = datetime.now()
        db.commit()
        db.refresh(db_item)
    return db_item

# Auth functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(db, username: str, password: str):
    user = get_user_by_email(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def access_token(db: Session, username: str, password: str):
    user = authenticate_user(db, username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    userdata = {
        'id': user.id,
        'email': user.email,
        'is_active': user.is_active,
        'created_at': user.created_at
    }

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    refreshdata = {'token_type': 'refresh', 'id': user.id}
    refresh_token = create_access_token(
        refreshdata, expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": userdata
    }

def create_login_token(user: models.User, refresh_token: str):
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    userdata = {
        'id': user.id,
        'email': user.email,
        'is_active': user.is_active,
        'created_at': user.created_at
    }

    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": userdata
    }

def get_access_from_refresh_token(db: Session, refresh_token: str):
    payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
    token_data = schemas.TokenPayload(**payload)
    token_user = get_user(db, token_data.id)

    return token_user
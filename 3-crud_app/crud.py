from fastapi import HTTPException
from sqlalchemy.orm import Session

import models, schemas

from datetime import datetime

# Users functions
## C: Create users
def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password, created_at=datetime.now())
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
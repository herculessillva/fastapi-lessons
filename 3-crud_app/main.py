from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

description = """
API desenvolvida para a disciplina de Programação Avançada. 🚀

## Users

You will be able to:

* **Create users**.
* **Read users**.
* **Update users**.
* **Delete users**.

## Items

You will be able to:

* **Create items**.
* **Read items**.
* **Update items**.
* **Delete items**.
"""

tags_metadata = [
    {
        "name": "Users",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "Items",
        "description": "Manage items. So _fancy_ they have their own docs.",
    },
]

app = FastAPI(title="API - Prog. Avançada",
                description=description,
                version="0.0.1",
                contact={
                    "name": "Hércules Silva",
                    "url": "https://github.com/herculessillva",
                    "email": "herculessilva@lapisco.ifce.edu.br",
                },
                license_info={
                    "name": "Apache 2.0",
                    "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
                },
                openapi_tags=tags_metadata)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Users methods
@app.post("/users/", response_model=schemas.User, tags=["Users"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User], tags=["Users"])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User, tags=["Users"])
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    print(db_user)
    return db_user

@app.put("/users/{id}", tags=["Users"])
def update_user(user_id: int, name: str):
    return None

@app.delete("/users/{id}", tags=["Users"])
def deletee_user(user_id: int, db: Session = Depends(get_db)):
    return crud.delete_user(db, user_id=user_id)


# Items methods
@app.post("/users/{user_id}/items/", response_model=schemas.Item, tags=["Items"])
def create_item_for_user(user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_user_item(db=db, item=item, user_id=user_id)

@app.get("/items/{item_id}", response_model=schemas.Item, tags=["Items"])
def read_item(item_id: int, db: Session = Depends(get_db)):
    return crud.get_item(db, item_id=item_id)

@app.get("/items/", response_model=List[schemas.Item], tags=["Items"])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_items(db, skip=skip, limit=limit)

@app.get("/users/{user_id}/items/", response_model=List[schemas.Item], tags=["Items"])
def read_items_by_user(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_items_by_users(db, user_id=user_id, skip=skip, limit=limit)

@app.put("/items/{item_id}", response_model=schemas.Item, tags=["Items"])
def update_item(item_id: int, title: str, description: str, owner_id: int, db: Session = Depends(get_db)):
    return crud.update_item(db, item_id=item_id, title=title, description=description, owner_id=owner_id)

@app.delete("/items/{item_id}", tags=["Items"])
def delete_item(item_id: int, db: Session = Depends(get_db)):
    return crud.delete_item(db, item_id=item_id)
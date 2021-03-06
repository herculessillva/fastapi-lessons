from typing import List, Optional

from pydantic import BaseModel

from datetime import datetime

class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int
    created_at: datetime = None
    updated_at: Optional[datetime] = None
    discarded_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    discarded_at: Optional[datetime] = None
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str
    user: User

class TokenData(BaseModel):
    username: Optional[str] = None

class TokenItem(BaseModel):
    refresh_token: str

class TokenPayload(BaseModel):
    token_type: Optional[str] = None
    id: Optional[int] = None
    exp: Optional[int] = None
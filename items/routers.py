from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from items.models import ItemDB
from database import get_db
from auth import get_user, get_password_hash
from items.schemas import ItemCreate, ItemResponse
from auth import (
    get_password_hash,
    get_user,
    authenticate_user,
    create_access_token,
    get_current_active_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from users.schemas import User


router = APIRouter()


@router.get("/items")
async def read_own_items(current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    items = db.query(ItemDB).filter(ItemDB.owner_id == current_user.id).all()
    return items

@router.post("/items", response_model=ItemResponse)
async def create_item(item: ItemCreate, current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    db_item = ItemDB(item_id=item.item_id, owner_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

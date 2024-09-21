from pydantic import BaseModel, EmailStr


class ItemCreate(BaseModel):
    item_id: str

class ItemResponse(ItemCreate):
    id: int

    class Config:
        from_attributes = True

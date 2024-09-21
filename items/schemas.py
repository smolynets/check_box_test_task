from enum import Enum
from uuid import UUID
from pydantic import BaseModel, EmailStr, condecimal


class ItemCreate(BaseModel):
    item_id: str

class ItemResponse(ItemCreate):
    id: int

    class Config:
        from_attributes = True


class PaymentTypeEnum(str, Enum):
    CASH = "cash"
    CASHLESS = "cashless"


class PaymentCreate(BaseModel):
    pay_type: PaymentTypeEnum
    amount: condecimal(gt=0, max_digits=10, decimal_places=2)


class PaymentResponse(PaymentCreate):
    id: UUID

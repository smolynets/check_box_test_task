from enum import Enum
from uuid import UUID
from pydantic import BaseModel, EmailStr, condecimal, computed_field, ValidationError, model_validator
from typing import List, Optional, Dict, Any
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime


class ProductCreate(BaseModel):
    name: str
    price_per_unit: condecimal(gt=0, max_digits=10, decimal_places=2)
    quantity: Optional[condecimal(gt=0, max_digits=10, decimal_places=2)] = None
    weight: Optional[condecimal(gt=0, max_digits=10, decimal_places=2)] = None

    @model_validator(mode='before')
    def check_quantity_or_weight(cls, values):
        if isinstance(values, dict):
            quantity = values.get('quantity')
            weight = values.get('weight')

            if not quantity and not weight:
                raise ValueError('Select quantity or weight - one of them.')
            if quantity and weight:
                raise ValueError('Select quantity or weight - not both of them.')
        return values


    @computed_field
    def product_total(self) -> Decimal:
        """
        Get total price of particular product in payment
        """
        product_value = self.price_per_unit * self.quantity if self.quantity else self.price_per_unit * self.weight
        total_value = product_value
        return total_value.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


class PaymentTypeEnum(str, Enum):
    CASH = "cash"
    CASHLESS = "cashless"


class PaymentCreate(BaseModel):
    pay_type: PaymentTypeEnum
    amount: condecimal(gt=0, max_digits=10, decimal_places=2)
    products: List[ProductCreate]
    additional_data: Optional[Dict[str, Any]] = None

    @computed_field
    def payment_total(self) -> Decimal:
        """
        Get total price of all product in payment
        """
        total_value = sum([x.product_total for x in self.products])
        return total_value.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    @computed_field
    def rest(self) -> Decimal:
        """
        Get rest money 
        """
        if self.amount > self.payment_total:
            rest = self.amount - self.payment_total
            return rest.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return 0


class PaymentResponse(PaymentCreate):
    id: UUID
    products: List[ProductCreate]
    additional_data: Optional[Dict[str, Any]] = None
    created_at: datetime

    class Config:
        orm_mode = True

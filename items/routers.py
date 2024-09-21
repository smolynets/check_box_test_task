from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from items.models import Payment
from database import get_db
from auth import get_user, get_password_hash
from items.schemas import ItemCreate, ItemResponse, PaymentCreate, PaymentResponse
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


@router.post("/payments/", response_model=PaymentResponse)
def create_payment(
    payment: PaymentCreate, current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)
    ):
    try:
        new_payment = Payment(
            pay_type=payment.pay_type,
            amount=payment.amount,
            owner_id=current_user.id,
            additional_data=payment.additional_data
        )
        db.add(new_payment)
        db.commit()
        db.refresh(new_payment)
        return new_payment
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()


@router.get("/payments")
async def read_payments(current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    payments = db.query(Payment).filter(Payment.owner_id == current_user.id).all()
    return payments

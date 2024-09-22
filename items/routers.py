from uuid import UUID
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session, joinedload
from fastapi.security import OAuth2PasswordRequestForm

from items.models import Payment, Product
from database import get_db
from auth import get_user, get_password_hash
from items.schemas import PaymentCreate, PaymentResponse
from auth import (
    get_password_hash,
    get_user,
    authenticate_user,
    create_access_token,
    get_current_active_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from users.schemas import User
from users.models import UserDB
from items.utils import PaymentFormatter


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
            additional_data=payment.additional_data,
            rest=payment.rest,
            payment_total=payment.payment_total
        )
        db.add(new_payment)
        db.commit()
        db.refresh(new_payment)
        for product_data in payment.products:
            new_product = Product(
                name=product_data.name,
                price_per_unit=product_data.price_per_unit,
                quantity=product_data.quantity,
                weight=product_data.weight,
                payment_id=new_payment.id,
                product_total=product_data.product_total
            )
            db.add(new_product)
        new_payment.payment_total=payment.payment_total
        db.commit()
        db.refresh(new_payment)
        new_payment = db.query(Payment).options(joinedload(Payment.products)).filter(
            Payment.id == new_payment.id
        ).first()
        return new_payment
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()


@router.get("/payments")
async def read_payments(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    pay_type: str = Query(None),
    start_date: datetime = Query(None),
    end_date: datetime = Query(None),
    min_total: float = Query(None),
    max_total: float = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, gt=0)
):
    """
    use date filter - /items/payments?start_date=2024-08-01&end_date=2024-08-01'
    """
    query = db.query(Payment).options(joinedload(Payment.products)).filter(
        Payment.owner_id == current_user.id
    )
    if pay_type:
        query = query.filter(Payment.pay_type == pay_type)
    if start_date:
        query = query.filter(Payment.created_at >= start_date)
    if end_date:
        query = query.filter(Payment.created_at <= end_date)
    if min_total is not None:
        query = query.filter(Payment.payment_total >= min_total)
    if max_total is not None:
        query = query.filter(Payment.payment_total <= max_total)
    payments = query.all()
    offset = (page - 1) * page_size
    payments = query.offset(offset).limit(page_size).all()
    return payments


@router.get("/payments/{id}")
async def get_payment_by_id(
    payment_id: UUID, current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)
):
    payment = db.query(Payment).options(joinedload(Payment.products)).filter(
        Payment.owner_id == current_user.id,
        Payment.id == payment_id
    ).first()
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment


@router.get("/payment/{receipt_link}")
def get_payment(receipt_link: str, line_width: int = 32, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.receipt_link == receipt_link).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Receipt not found")
    owner = db.query(UserDB).filter(UserDB.id == payment.owner_id).first()
    formatter = PaymentFormatter(payment, owner, line_width)
    return {"receipt_text": formatter.format_receipt()}

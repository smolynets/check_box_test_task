import enum
import uuid
import random
import string
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, Numeric, JSON, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base

def generate_unique_link():
    """
    Creation the unique link for payment
    """
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))


class Payment(Base):
    __tablename__ = 'payments'

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    pay_type = Column(String, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    additional_data = Column(JSON)
    products = relationship("Product", back_populates="payment")
    payment_total = Column(Numeric(10, 2), nullable=False)
    rest = Column(Numeric(10, 2))
    receipt_link = Column(String, unique=True, default=generate_unique_link, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    def __str__(self):
        return f"<Payment(id={self.id}, type={self.type}, amount={self.amount})>"


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    price_per_unit = Column(Numeric(10, 2), nullable=False)
    quantity = Column(Numeric(10, 2))
    weight = Column(Numeric(10, 2))
    payment_id = Column(UUID(as_uuid=True), ForeignKey('payments.id'), nullable=False)
    payment = relationship("Payment", back_populates="products")
    product_total = Column(Numeric(10, 2), nullable=False)

    def __str__(self):
        return f"<Product(id={self.id}, name={self.name}, price={self.price_per_unit}, quantity={self.quantity})>"

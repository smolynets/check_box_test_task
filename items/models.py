import enum
import uuid
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, Numeric, JSON
from sqlalchemy.dialects.postgresql import UUID

from database import Base


class Payment(Base):
    __tablename__ = 'payments'

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    pay_type = Column(String, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    additional_data = Column(JSON)

    def __str__(self):
        return f"<Payment(id={self.id}, type={self.type}, amount={self.amount})>"

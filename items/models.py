import enum
import uuid
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID

from database import Base


class ItemDB(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

#####

class Payment(Base):
    __tablename__ = 'payments'

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    pay_type = Column(String, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))

    def __str__(self):
        return f"<Payment(id={self.id}, type={self.type}, amount={self.amount})>"

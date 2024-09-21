from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from database import Base


class ItemDB(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
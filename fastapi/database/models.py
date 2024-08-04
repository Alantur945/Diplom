
from datetime import datetime
from .base import Base
from sqlalchemy import Boolean, DateTime, Float, Integer, String, Column, ForeignKey
from sqlalchemy.orm import relationship

class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, index=True)
    token = Column(String(255), unique=True)
    user = Column(ForeignKey("users.id"))


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, index=True)
    username = Column(String(255))
    password = Column(String(255))
    is_admin = Column(Boolean, default=False)


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, index=True)
    name = Column(String(255))
    articule = Column(String(255), unique=True)
    description = Column(String(255))
    price = Column(Float)
    photo = Column(String(100))
    date = Column(DateTime, default=datetime.now())
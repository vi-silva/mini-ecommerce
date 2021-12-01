from os import name
from sqlalchemy.sql.sqltypes import Boolean, Float, Integer, String, SmallInteger
from app.db.db import Base
from sqlalchemy import Column

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    description = Column(String(150))
    price = Column(Float(10, 2)) #numero com 10 antes e dois depois da virgula
    technical_details = Column(String(255))
    image = Column(String(255))
    visible = Column(Boolean, default=True)

class Supplier(Base):
    __tablename__ = 'suppliers'

    id = Column(Integer, primary_key=True)
    name = Column(String(45))

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(45))

class PaymentMethods(Base):
    __tablename__ = 'payment_methods'

    id = Column(Integer, primary_key= True)
    name = Column(String(45))
    enabled = Column(SmallInteger())

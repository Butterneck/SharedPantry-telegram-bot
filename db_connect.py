from sqlalchemy import create_engine, MetaData, Table, String, Float, Integer
from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime


Base = declarative_base()


class UserProduct(Base):
    __tablename__ = 'UserProducts'
    User_id = Column(Integer(), ForeignKey("Users.id"))
    ProductId = Column(Integer(), ForeignKey("Prodotti.id"))
    Quantita = Column(Integer())

class User(Base):
    __tablename__ = 'Users'
    id = Column(Integer(), primary_key=True)
    Username = Column(String(255), nullable=False)


class Prodotto(Base):
    __tablename__ = 'Prodotti'
    id = Column(Integer(), primary_key=True)
    Name = Column(String(255), nullable=False)
    Price = Column(Float(), nullable=False)
    Quantity = Column(Integer(), nullable=False)

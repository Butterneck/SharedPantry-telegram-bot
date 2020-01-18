from sqlalchemy import Column, Integer, DateTime, ForeignKey
from src.DB.DBManager.db_manager import Base


class Transaction(Base):

    __tablename__ = 'Transactions'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    date = Column(DateTime, nullable=False)
    quantity = Column(Integer, nullable=False)

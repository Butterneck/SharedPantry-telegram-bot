from sqlalchemy import Column, Integer, String
from src.DB.DBManager.db_manager import Base


class User(Base):

    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False, unique=True)
    chat_id = Column(Integer, nullable=False, unique=True)

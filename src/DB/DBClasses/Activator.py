from sqlalchemy import Column, Integer, Boolean
from src.DB.DBManager.db_manager import Base

class Activator(Base):

    __tablename__ = 'Activators'

    id = Column(Integer, primary_key=True)
    activator = Column(Boolean, nullable=False)

from sqlalchemy import Column, Integer, Boolean
from src.DB.DBManager.db_manager import Base


class Backup(Base):

    __tablename__ = 'Backups'

    id = Column(Integer, primary_key=True)
    backup = Column(Boolean)

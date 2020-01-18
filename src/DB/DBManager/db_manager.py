from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DB_Manager():

    def __init__(self, db_url, sslRequired):
        self.engine =  create_engine(db_url)

        # Need to import those classes after Base declaration to avoid importing errors
        from src.DB.DBClasses.Activator import Activator
        from src.DB.DBClasses.Backup import Backup
        from src.DB.DBClasses.Debit import Debit
        from src.DB.DBClasses.Product import Product
        from src.DB.DBClasses.User import User
        from src.DB.DBClasses.Transaction import Transaction

        # Creating schema
        Base.metadata.create_all(self.engine)

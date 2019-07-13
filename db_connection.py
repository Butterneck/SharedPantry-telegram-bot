from sqlalchemy import create_engine

db

def connect():
    db = create_engine('sqlite:///disopensa.db', echo=True)

def disconnect():
    db.close()

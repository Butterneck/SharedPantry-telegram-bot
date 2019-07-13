from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float

Base = declarative_base()

class Prodotto(Base):
    __tablename__ = "Prodotti"


    def __init__(self, id, nome, quantita, prezzo):
        self.nome = nome
        self.quantita = quantita
        self.prezzo = prezzo


    id = Column(Integer, primary_key=True)
    nome = Column(String)
    quantita = Column(Integer)
    prezzo = Column(Float)

    Utente = relationship("User_Prodotti", back_populates="Prodotti")

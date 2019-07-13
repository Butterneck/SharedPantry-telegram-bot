from os import path
import sqlite3
from Utils import *
import datetime

from User import *
from User_Prodotti import *
from Prodotti import *

DB_PATH = "dispensa.db"
init_db = open("dispensa.sql").read()

class DB_Connection():
    def __init__(self):
        self.path = DB_PATH
        self.connection = None
        self.db = None
        if path.isfile(self.path):
            self.connection = sqlite3.connect(DB_PATH)
            self.db = self.connection.cursor()
            print(terminalColors.OKGREEN + '[Database]: ' + self.path + ' open' + terminalColors.ENDC)
        else:
            print(terminalColors.OKGREEN + '[Database]: ' + self.path + ' not found' + terminalColors.ENDC)
            print(terminalColors.OKGREEN + '[Database]: ' + self.path + ' initialization' + terminalColors.ENDC)
            self.connection = sqlite3.connect(DB_PATH)
            self.db = self.connection.cursor()
            self.db.executescript(init_db)
            self.connection.commit()

    def __del__(self):
        if self.connection != None:
            self.connection.close()
            print(terminalColors.OKGREEN + '[Database]: ' + self.path + ' closed' + terminalColors.ENDC)

    def existDB(self):
        return path.isfile(self.path)

    def startDB(self):
        if self.existDB() == False:
            print(terminalColors.OKGREEN + '[Database]: ' + self.path + ' initialization' + terminalColors.ENDC)
            self.db.executescript(init_db)
            self.connection.commit()
        else:
            print(terminalColors.OKGREEN + '[Database]: ' + self.path + '...OK' + terminalColors.ENDC)

    def addUser(self, username, chat_id):
        if self.existDB():
            print(terminalColors.OKGREEN + '[Database]: ' + self.path + '...OK' + terminalColors.ENDC)
            self.db.execute('INSERT INTO Users VALUES(?, ?);', (username, chat_id))
            return User(self.db.lastrowid, username, chat_id)
        else:
            print(terminalColors.FAIL + '[Error]-[Database]: '+ self.path +' not found' + terminalColors.ENDC)
            return None

    def addProduct(self, name, price, qt):
        if self.existDB():
            print(terminalColors.OKGREEN + '[Database]: ' + self.path + '...OK' + terminalColors.ENDC)
            self.db.execute('INSERT INTO Prodotti VALUES(?, ?, ?);', (name, price, qt))
            self.connection.commit()
            return Product(self.db.lastrowid, name, price, qt)
        else:
            print(terminalColors.FAIL + '[Error]-[Database]: '+ self.path +' not found' + terminalColors.ENDC)
            return None

    def modifyQuantity(self, product_id, qt):
            if self.existDB():
                print(terminalColors.OKGREEN + '[Database]: ' + self.path + '...OK' + terminalColors.ENDC)
                self.db.execute('UPDATE Prodotti SET Quantity = ? WHERE rowid = ?;', (qt, product_id))
                #return Product(product_id, )
            else:
                print(terminalColors.FAIL + '[Error]-[Database]: '+ self.path +' not found' + terminalColors.ENDC)
                return None

    def addTransaction(self, username_id, product_id, qt):
        if self.existDB():
            year = datetime.date.today().year
            month = datetime.date.today().month
            day = datetime.date.today().day
            d = datetime.date(year, month, day)
            print(terminalColors.OKGREEN + '[Database]: ' + self.path + '...OK' + terminalColors.ENDC)
            self.db.execute('INSERT INTO User_Prodotti VALUES(?, ?, ?, ?);', (username_id, product_id, d, qt))
            self.connection.commit()
            self.db.execute('SELECT Quantity FROM Prodotti WHERE rowid = ?', (product_id, ))
            lastQuantity = int(self.db.fetchone()[0]);
            if lastQuantity-qt >= 0:
                #Ci sono ancora, aggiorno semplicemente
                self.modifyQuantity(product_id, lastQuantity-qt)
            else:
                #Prodotto è finit, impsoto la quantità a 0
                self.modifyQuantity(product_id, 0)
            return User_Prodotti(self.db.lastrowid, username_id, product_id, d, qt)
        else:
            print(terminalColors.FAIL + '[Error]-[Database]: '+ self.path +' not found' + terminalColors.ENDC)
            return None

    def getUserId(self, username):
        if self.existDB():
            print(terminalColors.OKGREEN + '[Database]: ' + self.path + '...OK' + terminalColors.ENDC)
            self.db.execute('SELECT rowid FROM Users WHERE Username = ?', (username, ))
            return int(self.db.fetchone()[0])
        else:
            print(terminalColors.FAIL + '[Error]-[Database]: '+ self.path +' not found' + terminalColors.ENDC)
            return None

    def getAllProduct(self):
        if self.existDB():
            prodotti = []
            print(terminalColors.OKGREEN + '[Database]: ' + self.path + '...OK' + terminalColors.ENDC)
            self.db.execute('SELECT rowid, * FROM Prodotti')
            query = self.db.fetchall()
            for el in query:
                prodotti.append(Product(el[0], el[1], el[2], el[3]))
            return prodotti
        else:
            print(terminalColors.FAIL + '[Error]-[Database]: '+ self.path +' not found' + terminalColors.ENDC)
            return None

    def getAllChatIds(self):
        if self.existDB():
            chat_ids = []
            print(terminalColors.OKGREEN + '[Database]: ' + self.path + '...OK' + terminalColors.ENDC)
            self.db.execute('SELECT chat_id FROM Users')
            query = self.db.fetchall()
            for el in query:
                chat_ids.append(el[0])
            return chat_ids
        else:
            print(terminalColors.FAIL + '[Error]-[Database]: '+ self.path +' not found' + terminalColors.ENDC)
            return None

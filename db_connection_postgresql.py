from os import path
import sqlite3
from Utils import *
import datetime
import psycopg2
import os


from User import *
from User_Prodotti import *
from Prodotti import *
from Debiti import Debit
from Activator import Activator

#DB_URL = "postgres://eyicwwxwnxuxou:675f943b8955a12022eab26b184c193d3c1219c4999688d899cfb3687f33e1b4@ec2-54-217-234-157.eu-west-1.compute.amazonaws.com:5432/df8fia9ccanh45"
init_db = open("dispensa.sql").read()

intro = terminalColors.OKGREEN + '[Database]: '
end = terminalColors.ENDC


class DB_Connection():
    # Da modificare quando verrà portato su heroku
    # DB_URL = os.environ['DATABASE_URL']


    def __init__(self, DB_URL):
        self.path = DB_URL
        self.connection = psycopg2.connect(DB_URL, sslmode='require')
        self.db = self.connection.cursor()
        self.db.execute( "SELECT EXISTS (   SELECT 1   FROM   information_schema.tables    WHERE  table_schema = 'schema_name'   AND    table_name = 'users' OR table_name='user_prodotti' OR table_name='prodotti' OR table_name='debits' OR table_name='activator');")
        if self.db.fetchone()[0]:
            print(intro + self.path  + self.path  + ' already exists' + end)
        else:
            print(intro + self.path  + ' not found' + end)
            print(intro + self.path  + ' initialization' + end)
            self.db.execute(init_db)
            self.connection.commit()

    def __del__(self):
        if self.connection != None:
            self.connection.close()
            print(intro + self.path  + ' closed' + end)

    def existDB(self):
        self.db.execute( "SELECT EXISTS (   SELECT 1   FROM   information_schema.tables    WHERE  table_schema = 'schema_name'   AND    table_name = 'users' OR table_name='user_prodotti' OR table_name='prodotti' OR table_name='debits' OR table_name='activator');")
        return self.db.fetchone()[0]

    def startDB(self):
        if self.existDB() == False:
            print(intro + self.path  + ' initialization' + end)
            self.db.execute(init_db)
            self.connection.commit()
        else:
            print(intro + self.path  + '...OK' + end)

    def addUser(self, username, chat_id):
        if self.existDB():
            print(intro + self.path  + '...Aggiunta untente' + end)
            self.db.execute('INSERT INTO Users(Username, Chat_Id) VALUES(%s, %s) RETURNING Id;', (username, chat_id))
            self.connection.commit()
            return User(self.db.fetchone()[0], username, chat_id)
        else:
            print(terminalColors.FAIL + '[Error]-[Database]: '+ self.path +' not found' + end)
            return None

    def removeUser(self, chat_id):
        if self.existDB():
            print(intro + self.path  + '...Rimuozione utente' + end)
            uid = str(self.getuserId_fromChatId(chat_id))
            self.db.execute('DELETE FROM Prodotti WHERE Id = %s;', (uid, ))
            self.connection.commit()
            return True
        else:
            print(terminalColors.FAIL + '[Error]-[Database]: '+ self.path +' not found' + end)
            return False

    def addProduct(self, name, price, qt):
        if self.existDB():
            print(intro + self.path  + '...Aggiunta prodotto' + end)
            self.db.execute('INSERT INTO Prodotti(Name, Price, Quantity) VALUES(%s, %s, %s) RETURNING Id;', (name, price, qt))
            self.connection.commit()
            return Product(self.db.fetchone()[0], name, price, qt)
        else:
            print(terminalColors.FAIL + '[Error]-[Database]: '+ self.path +' not found' + end)
            return None

    def removeProduct(self, product_id):
        if self.existDB():
            print(intro + self.path  + '...Rimuovi prodotto' + end)
            self.db.execute('DELETE FROM Prodotti WHERE Id = %s;', (product_id, ))
            self.connection.commit()
            return True
        else:
            print(terminalColors.FAIL + '[Error]-[Database]: '+ self.path +' not found' + end)
            return False

    def modifyQuantity(self, product_id, qt):
            if self.existDB():
                print(intro + self.path  + '...Modifica quantità' + end)
                self.db.execute('UPDATE Prodotti SET Quantity = %s WHERE Id = %s;', (qt, product_id))
                self.connection.commit()
                #return Product(product_id, )
            else:
                print(terminalColors.FAIL + '[Error]-[Database]: '+ self.path +' not found' + end)
                return None

    def addTransaction(self, chat_id, product_id, qt):
        if self.existDB():
            d = datetime.date.today()
            uid = self.getuserId_fromChatId(chat_id)
            print(intro + self.path  + '...Aggiunta transazione' + end)
            self.db.execute('SELECT Quantity FROM Prodotti WHERE Id = %s', (product_id, ))
            lastQuantity = int(self.db.fetchone()[0]);

            if lastQuantity == 0:
                #Eccezione
                raise Exception("Acquisto non possibile")

            if lastQuantity-qt >= 0:
                #Ci sono ancora, aggiorno semplicemente
                self.db.execute('INSERT INTO User_Prodotti(User_Id, Prodotto_Id, Data, Quantity) VALUES(%s, %s, %s, %s);', (uid, product_id, d, qt))
                self.connection.commit()
                self.modifyQuantity(product_id, lastQuantity-qt)
            else:
                #Prodotto è finit, impsoto la quantità a 0
                self.modifyQuantity(product_id, 0)
            return User_Prodotti(self.db.lastrowid, uid, product_id, d, qt)
        else:
            print(terminalColors.FAIL + '[Error]-[Database]: ' + self.path + ' not found' + end)
            return None

    def removeTransaction(self, transaction_id):
        if self.existDB():
            print(intro + self.path  + '...Rimozione transazione' + end)
            self.db.execute('DELETE FROM User_Prodotti WHERE Id = %s;', (transaction_id, ))
            self.connection.commit()
            return True
        else:
            print(terminalColors.FAIL + '[Error]-[Database]: ' + self.path + ' not found' + end)
            return False

    def getUserId(self, username):
        if self.existDB():
            print(intro + self.path  + '...getUserId' + end)
            self.db.execute('SELECT Id FROM Users WHERE Username = %s', (username, ))
            return int(self.db.fetchone()[0])
        else:
            print(terminalColors.FAIL + '[Error]-[Database]: '+ self.path +' not found' + end)
            return None

    def getuserId_fromChatId(self, chat_id):
        if self.existDB():
            print(intro + self.path  + '...getUserId_fromChatId' + end)
            self.db.execute('SELECT Id FROM Users WHERE Chat_Id = %s', (chat_id, ))
            query = self.db.fetchone()
            if query is not None:
                return query[0]
            else:
                return None
        else:
            print(terminalColors.FAIL + '[Error]-[Database]: '+ self.path +' not found' + end)
            return None

        def getUsername_fromChatId(self, chat_id):
            if self.existDB():
                print(intro + self.path  + '...getUsername_fromChatId' + end)
                self.db.execute('SELECT Username FROM Users WHERE Chat_Id = %s', (chat_id, ))
                query = self.db.fetchone()
                if query is not None:
                    return query[0]
                else:
                    return None
            else:
                print(terminalColors.FAIL + '[Error]-[Database]: '+ self.path +' not found' + end)
                return None


    def getAllProduct(self):
        if self.existDB():
            prodotti = []
            print(intro + self.path  + '...getAllProduct' + end)
            self.db.execute('SELECT * FROM Prodotti')
            query = self.db.fetchall()
            for el in query:
                prodotti.append(Product(el[0], el[1], el[2], el[3]))
            return prodotti
        else:
            print(terminalColors.FAIL + '[Error]-[Database]: '+ self.path +' not found' + end)
            return None

    def getAllChatIds(self):
        if self.existDB():
            chat_ids = []
            print(intro + self.path  + '...getAllChatIds' + end)
            self.db.execute('SELECT Chat_Id FROM Users')
            query = self.db.fetchall()
            for el in query:
                chat_ids.append(el[0])
            return chat_ids
        else:
            print(terminalColors.FAIL + '[Error]-[Database]: '+ self.path +' not found' + end)
            return None

    def getAllAcquisti(self, chat_id):
        if self.existDB():
            acquisti = []
            uid = self.getuserId_fromChatId(chat_id)
            print(intro + self.path  + '...getAllAcquisti' + end)
            self.db.execute('SELECT * FROM User_Prodotti WHERE User_Id = %s', (uid, ))
            query = self.db.fetchall()
            for el in query:
                acquisti.append(User_Prodotti(el[0], el[1], el[2], el[3], el[4]))
            return acquisti
        else:
            print(terminalColors.FAIL + '[Error]-[Database]: '+ self.path +' not found' + end)
            return None

    def getAcquistiIn(self, chat_id, data_inizio, data_fine):
        if self.existDB():
            acquisti = []
            uid = self.getuserId_fromChatId(chat_id)
            print(intro + self.path  + '...getAcquistiIn' + end)
            self.db.execute('SELECT * FROM User_Prodotti WHERE User_Id = %s AND Data >= %s AND Data <= %s', (uid, data_inizio, data_fine))
            query = self.db.fetchall()
            for el in query:
                acquisti.append(User_Prodotti(el[0], el[1], el[2], el[3], el[4]))
            return acquisti
        else:
            print(terminalColors.FAIL + '[Error]-[Database]: '+ self.path +' not found' + end)
            return None

    def getAllDebits(self):
        if self.existDB():
            acquisti = []
            print(intro + self.path  + '...getAllAcquisti' + end)
            self.db.execute('SELECT * FROM User_Prodotti')
            query = self.db.fetchall()
            for el in query:
                acquisti.append(User_Prodotti(el[0], el[1], el[2], el[3], el[4]))
            return acquisti
        else:
            print(terminalColors.FAIL + '[Error]-[Database]: '+ self.path +' not found' + end)
            return None

    def getAllusers(self):
        if self.existDB():
            utenti = []
            print(intro + self.path  + '...getAcquistiIn' + end)
            self.db.execute('SELECT * FROM Users')
            query = self.db.fetchall()
            for el in query:
                utenti.append(User(el[0], el[1], el[2]))
            return utenti
        else:
            print(terminalColors.FAIL + '[Error]-[Database]: '+ self.path +' not found' + end)
            return None

    def dropAllTables(self):
        if self.existDB():
            print(terminalColors.WARNING + '[Database]: ' + self.path + '... Dropping tables' + end)
            self.db.execute('DROP TABLE IF EXISTS users, prodotti, user_prodotti;')
            self.connection.commit()
            self.db.execute(init_db)
            self.connection.commit()
            print(intro + self.path  + ' initialization' + end)
            return True
        else:
            print(terminalColors.FAIL + '[Error]-[Database]: ' + self.path + ' not found' + end)
            return False

    def deactivateActivator(self):
        if self.existDB():
            print(intro + self.path  + '...deactivateActivator' + end)
            self.db.execute('UPDATE Activator SET Activator = 1')
            self.connection.commit()
        else:
            print(intro + self.path  + ' not found' + end)

    def checkActivator(self):
        if self.existDB():
            print(intro + self.path  + '...checkActivator' + end)
            self.db.execute('SELECT Activator FROM Activator')
            if self.db.fetchone():
                print(intro + self.path  + ' activator activated' + end)
                return True
            return False
        else:
            print(intro + self.path  + ' not found' + end)
            print(intro + self.path  + ' initializing activator' + end)
            deactivateActivator()
            return False

    def cleanCursor(self):
        self.connection.commit()

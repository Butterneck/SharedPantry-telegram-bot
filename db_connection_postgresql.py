from os import path
import sqlite3
from Utils import *
import datetime
import psycopg2
import os
from sys import exit


from User import *
from User_Prodotti import *
from Prodotti import *
from Debiti import Debit
from Activator import Activator
from Backup import Backup

#DB_URL = "postgres://eyicwwxwnxuxou:675f943b8955a12022eab26b184c193d3c1219c4999688d899cfb3687f33e1b4@ec2-54-217-234-157.eu-west-1.compute.amazonaws.com:5432/df8fia9ccanh45"
init_db = open("dispensa.sql").read()

intro = terminalColors.OKGREEN + '[Database]: '
end = terminalColors.ENDC


class DB_Connection():
    # Da modificare quando verrà portato su heroku
    # DB_URL = os.environ['DATABASE_URL']


    def __init__(self, DB_URL):
        self.path = DB_URL
        self.connection = None
        try:
            self.connection = psycopg2.connect(DB_URL, sslmode='require')
        except psycopg2.OperationalError as e:
            print(terminalColors.FAIL + "Database not reachable." + terminalColors.ENDC)
            print(terminalColors.FAIL + "Exit" + terminalColors.ENDC)
            exit(1)
        else:
            print(terminalColors.OKGREEN + "[Database]: reachable")

        self.db = self.connection.cursor()
        self.db.execute( "SELECT EXISTS (   SELECT 1   FROM   information_schema.tables    WHERE  table_schema = 'schema_name'   AND    table_name = 'users' OR table_name='user_prodotti' OR table_name='prodotti' OR table_name='debits' OR table_name='activator' OR table_name='backup');")
        if self.db.fetchone()[0]:
            print(intro + 'Database already exists' + end)
        else:
            print(intro + 'not found' + end)
            print(intro + 'initialization' + end)
            self.db.execute(init_db)
            self.connection.commit()

    def __del__(self):
        if self.connection != None:
            self.connection.close()
            print(intro + ' closed' + end)

    def existDB(self):
        self.cleanCursor()
        self.db.execute( "SELECT EXISTS (   SELECT 1   FROM   information_schema.tables    WHERE  table_schema = 'schema_name'   AND    table_name = 'users' OR table_name='user_prodotti' OR table_name='prodotti' OR table_name='debits' OR table_name='activator' OR table_name='backup');")
        return self.db.fetchone()[0]

    def startDB(self):
        if self.existDB() == False:
            print(intro + ' initialization' + end)
            self.cleanCursor()
            self.db.execute(init_db)
            self.connection.commit()
        else:
            print(intro + '...OK' + end)

    def addUser(self, username, chat_id):
        if self.existDB():
            print(intro + '...Aggiunta untente' + end)
            self.cleanCursor()
            self.db.execute('INSERT INTO Users(Username, Chat_Id) VALUES(%s, %s) RETURNING Id;', (username, chat_id))
            self.connection.commit()
            return User(self.db.fetchone()[0], username, chat_id)
        else:
            print(terminalColors.FAIL + '[Error]-[Database]: '+ ' not found' + end)
            return None

    def removeUser(self, chat_id):
        if self.existDB():
            print(intro +  '...Rimuozione utente' + end)
            uid = str(self.getuserId_fromChatId(chat_id))
            self.cleanCursor()
            self.db.execute('DELETE FROM Prodotti WHERE Id = %s;', (uid, ))
            self.connection.commit()
            return True
        else:
            print(terminalColors.FAIL + '[Error]-[Database]: '+ ' not found' + end)
            return False

    def addProduct(self, name, price, qt):
        if self.existDB():
            print(intro + '...Aggiunta prodotto' + end)
            self.cleanCursor()
            self.db.execute('INSERT INTO Prodotti(Name, Price, Quantity) VALUES(%s, %s, %s) RETURNING Id;', (name, price, qt))
            self.connection.commit()
            return Product(self.db.fetchone()[0], name, price, qt)
        else:
            print(terminalColors.FAIL + '[Error]-[Database]: '+ ' not found' + end)
            return None

    def removeProduct(self, product_id):
        if self.existDB():
            print(intro + '...Rimuovi prodotto' + end)
            self.cleanCursor()
            self.db.execute('DELETE FROM Prodotti WHERE Id = %s;', (product_id, ))
            self.connection.commit()
            return True
        else:
            print(terminalColors.FAIL + '[Error]-[Database]: '+ ' not found' + end)
            return False

    def modifyQuantity(self, product_id, qt):
            if self.existDB():
                print(intro + '...Modifica quantità' + end)
                self.cleanCursor()
                self.db.execute('UPDATE Prodotti SET Quantity = %s WHERE Id = %s;', (qt, product_id))
                self.connection.commit()
                return True
            else:
                print(terminalColors.FAIL + '[Error]-[Database]: ' + ' not found' + end)
                return None

    def addTransaction(self, chat_id, product_id, qt):
        if self.existDB():
            d = datetime.date.today()
            uid = self.getuserId_fromChatId(chat_id)
            print(intro + '...Aggiunta transazione' + end)
            self.cleanCursor()
            self.db.execute('SELECT Quantity FROM Prodotti WHERE Id = %s', (product_id, ))
            lastQuantity = int(self.db.fetchone()[0]);

            if lastQuantity == 0:
                #Eccezione
                raise Exception("Acquisto non possibile")

            if lastQuantity-qt >= 0:
                #Ci sono ancora, aggiorno semplicemente
                self.cleanCursor()
                self.db.execute('INSERT INTO User_Prodotti(User_Id, Prodotto_Id, Data, Quantity) VALUES(%s, %s, %s, %s);', (uid, product_id, d, qt))
                self.connection.commit()
                self.modifyQuantity(product_id, lastQuantity-qt)
            else:
                #Prodotto è finit, impsoto la quantità a 0
                self.modifyQuantity(product_id, 0)
            return User_Prodotti(self.db.lastrowid, uid, product_id, d, qt)
        else:
            print(terminalColors.FAIL + '[Error]-[Database]: ' +  ' not found' + end)
            return None

    def removeTransaction(self, transaction_id):
        if self.existDB():
            print(intro + '...Rimozione transazione' + end)
            self.cleanCursor()
            self.db.execute('DELETE FROM User_Prodotti WHERE Id = %s;', (transaction_id, ))
            self.connection.commit()
            return True
        else:
            print(terminalColors.FAIL + '[Error]-[Database]: ' +  ' not found' + end)
            return False

    def getUserId(self, username):
        if self.existDB():
            print(intro + '...getUserId' + end)
            self.cleanCursor()
            self.db.execute('SELECT Id FROM Users WHERE Username = %s', (username, ))
            return int(self.db.fetchone()[0])
        else:
            print(terminalColors.FAIL + '[Error]-[Database]: '+ ' not found' + end)
            return None

    def getuserId_fromChatId(self, chat_id):
        if self.existDB():
            print(intro + '...getUserId_fromChatId' + end)
            self.cleanCursor()
            self.db.execute('SELECT Id FROM Users WHERE Chat_Id = %s', (chat_id, ))
            query = self.db.fetchone()
            if query is not None:
                return query[0]
            else:
                return None
        else:
            print(terminalColors.FAIL + '[Error]-[Database]: '+ ' not found' + end)
            return None

    def getUsername_fromChatId(self, chat_id):
        if self.existDB():
            print(intro + '...getUsername_fromChatId' + end)
            self.cleanCursor()
            self.db.execute('SELECT Username FROM Users WHERE Chat_Id = %s', (chat_id, ))
            query = self.db.fetchone()
            if query is not None:
                return query[0]
            else:
                return None
        else:
            print(terminalColors.FAIL + '[Error]-[Database]: '+ ' not found' + end)
            return None


    def getAllProduct(self):
        if self.existDB():
            prodotti = []
            print(intro + '...getAllProduct' + end)
            self.cleanCursor()
            self.db.execute('SELECT * FROM Prodotti')
            query = self.db.fetchall()
            for el in query:
                prodotti.append(Product(el[0], el[1], el[2], el[3]))
            return prodotti
        else:
            print(terminalColors.FAIL + '[Error]-[Database]: '+ ' not found' + end)
            return None

    def getAllChatIds(self):
        if self.existDB():
            chat_ids = []
            print(intro + '...getAllChatIds' + end)
            self.cleanCursor()
            self.db.execute('SELECT Chat_Id FROM Users')
            query = self.db.fetchall()
            for el in query:
                chat_ids.append(el[0])
            return chat_ids
        else:
            print(terminalColors.FAIL + '[Error]-[Database]: '+ ' not found' + end)
            return None

    def getAllAcquisti(self, chat_id):
        if self.existDB():
            acquisti = []
            uid = self.getuserId_fromChatId(chat_id)
            print(intro + '...getAllAcquisti' + end)
            self.cleanCursor()
            self.db.execute('SELECT * FROM User_Prodotti WHERE User_Id = %s', (uid, ))
            query = self.db.fetchall()
            for el in query:
                acquisti.append(User_Prodotti(el[0], el[1], el[2], el[3], el[4]))
            return acquisti
        else:
            print(terminalColors.FAIL + '[Error]-[Database]: '+ ' not found' + end)
            return None

    def getAcquistiIn(self, chat_id, data_inizio, data_fine):
        if self.existDB():
            acquisti = []
            uid = self.getuserId_fromChatId(chat_id)
            print(intro + '...getAcquistiIn' + end)
            self.cleanCursor()
            self.db.execute('SELECT * FROM User_Prodotti WHERE User_Id = %s AND Data >= %s AND Data <= %s', (uid, data_inizio, data_fine))
            query = self.db.fetchall()
            for el in query:
                acquisti.append(User_Prodotti(el[0], el[1], el[2], el[3], el[4]))
            return acquisti
        else:
            print(terminalColors.FAIL + '[Error]-[Database]: '+ ' not found' + end)
            return None

    def getAllDebits(self):
        if self.existDB():
            acquisti = []
            print(intro + '...getAllAcquisti' + end)
            self.cleanCursor()
            self.db.execute('SELECT * FROM User_Prodotti')
            query = self.db.fetchall()
            for el in query:
                acquisti.append(User_Prodotti(el[0], el[1], el[2], el[3], el[4]))
            return acquisti
        else:
            print(terminalColors.FAIL + '[Error]-[Database]: '+ ' not found' + end)
            return None

    def getAllusers(self):
        if self.existDB():
            utenti = []
            print(intro + '...getAcquistiIn' + end)
            self.cleanCursor()
            self.db.execute('SELECT * FROM Users')
            query = self.db.fetchall()
            for el in query:
                utenti.append(User(el[0], el[1], el[2]))
            return utenti
        else:
            print(terminalColors.FAIL + '[Error]-[Database]: '+ ' not found' + end)
            return None

    def dropAllTables(self):
        if self.existDB():
            print(terminalColors.WARNING + '[Database]: ' + '... Dropping tables' + end)
            self.cleanCursor()
            self.db.execute('DROP TABLE IF EXISTS users, prodotti, user_prodotti, debits, activator;')
            self.connection.commit()
            self.db.execute(init_db)
            self.connection.commit()
            print(intro +  ' initialization' + end)
            return True
        else:
            print(terminalColors.FAIL + '[Error]-[Database]: ' + ' not found' + end)
            return False

    def activateActivator(self):
        if self.existDB():
            print(intro + '...activateActivator' + end)
            self.cleanCursor()
            self.db.execute('UPDATE Activator SET Activator = 1')
            self.connection.commit()
        else:
            print(intro +  ' not found' + end)

    def deactivateActivator(self):
        if self.existDB():
            print(intro + '...deactivateActivator' + end)
            self.cleanCursor()
            self.db.execute('UPDATE Activator SET Activator = 0')
            self.connection.commit()
        else:
            print(intro +  ' not found' + end)

    def checkActivator(self):
        if self.existDB():
            print(intro +  '...checkActivator' + end)

            self.cleanCursor()
            self.db.execute('SELECT * FROM Activator')
            if len(self.db.fetchall()) == 0:
                print(intro +  '...createActivatorRow' + end)
                self.db.execute('INSERT INTO Activator(activator) VALUES(1)')
                self.connection.commit()

            self.db.execute('SELECT Activator FROM Activator')
            if self.db.fetchone()[0]:
                print(intro +  ' activator activated' + end)
                print('Done')
                return True
            print('Done')
            return False
        else:
            print(intro +  ' not found' + end)
            print(intro +  ' initializing activator' + end)
            self.deactivateActivator()
            return False

    def checkTransaction_forProducts(self, product_id):
        if self.existDB():
            print(intro + "...checkTransaction_forProducts" + end)
            self.cleanCursor()
            self.db.execute('SELECT * FROM User_Prodotti WHERE Prodotto_Id = %s;', (product_id, ))

            if len(self.db.fetchall()) != 0:
                print(intro +  "Prodotto non eliminabile, transazioni correlate" + end)
                return False
            else:
                print(intro +  "Prodotto eliminabile" + end)
                return True

    def activateBackup(self):
        if self.existDB():
            print(intro + self.path + '...activateBackup' + end)
            self.cleanCursor()
            self.db.execute('UPDATE Backup SET Backup = 1')
            self.connection.commit()
        else:
            print(intro +  'not found' + end)

    def deactivateBackup(self):
        if self.existDB():
            print(intro + '...deactivateBackup' + end)
            self.cleanCursor()
            self.db.execute('UPDATE Backup SET Backup = 0')
            self.connection.commit()
        else:
            print(intro +  'not found' + end)

    def checkBackup(self):
        if self.existDB():
            print(intro + '...checkBackup' + end)
            self.cleanCursor()
            self.db.execute('SELECT * FROM Backup')
            if len(self.db.fetchall()) == 0:
                print(intro +  '...createBackupRow' + end)
                self.db.execute('INSERT INTO Backup(backup) VALUES(1)')
                self.connection.commit()

            self.db.execute('SELECT Backup FROM Backup')
            if self.db.fetchone()[0]:
                print(intro +  ' backup activated' + end)
                print('Done')
                return True
            print('Done')
            return False
        else:
            print(intro +  ' not found' + end)
            print(intro +  ' initializing backup' + end)
            self.deactivateBackup()
            return False

    def cleanCursor(self):
        self.connection.rollback()


    def runSqlQuery(self, query):
        if self.existDB():
            print(terminalColors.WARNING + "Eseguendo query arbitraria:")
            print(str(query) + terminalColors.ENDC)
            self.db.execute(query)
            self.connection.commit()
            try:
                return self.db.fetchall()
            except:
                return True
        else:
            print(terminalColors.FAIL + '[Error]-[Database]: ' +  ' not found' + end)
            return None

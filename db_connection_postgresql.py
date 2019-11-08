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

init_db = open("dispensa.sql").read()

intro = terminalColors.OKGREEN + '[Database]: '
end = terminalColors.ENDC


def print_DB_unreachable(db_name):
    print(terminalColors.FAIL + '[Error]-[Database]: ' + db_name + ' not found' + end)


class DB_Connection():

    def __init__(self, DB_URL, db_name="Default"):
        self.path = DB_URL
        self.db_name = db_name
        self.connection = None
        try:
            self.connection = psycopg2.connect(DB_URL, sslmode='require')
        except psycopg2.OperationalError as e:
            print(terminalColors.FAIL + "Database " + self.db_name + " not reachable." + terminalColors.ENDC)
            print(terminalColors.FAIL + "Exit" + terminalColors.ENDC)
            exit(1)
        else:
            print(intro + self.db_name + " reachable")

        self.db = self.connection.cursor()
        self.db.execute(
            "SELECT EXISTS (   SELECT 1   FROM   information_schema.tables    WHERE  table_schema = 'schema_name'   AND    table_name = 'users' OR table_name='user_prodotti' OR table_name='prodotti' OR table_name='debits' OR table_name='activator' OR table_name='backup');")
        if self.db.fetchone()[0]:
            print(intro + self.db_name + ' already exists' + end)
        else:
            print(intro + self.db_name + ' not found' + end)
            print(intro + self.db_name + ' initialization' + end)
            self.db.execute(init_db)
            self.connection.commit()


    def __del__(self):
        if self.connection != None:
            self.connection.close()
            print(intro + self.db_name + ' closed' + end)

    def existDB(self):
        self.cleanCursor()
        try:
            self.db.execute("SELECT EXISTS (   SELECT 1   FROM   information_schema.tables    WHERE  table_schema = 'schema_name'   AND    table_name = 'users' OR table_name='user_prodotti' OR table_name='prodotti' OR table_name='debits' OR table_name='activator' OR table_name='backup');")
            return self.db.fetchone()[0]
        except:
            return False

    def startDB(self):
        if not self.existDB():
            print(intro + self.db_name + ' initialization' + end)
            self.cleanCursor()
            self.db.execute(init_db)
            self.connection.commit()
        else:
            print(intro + self.db_name + '...OK' + end)

    def addUser(self, username, chat_id):
        if self.existDB():
            print(intro + self.db_name + '...Aggiunta untente' + end)
            self.cleanCursor()
            self.db.execute('INSERT INTO Users(Username, Chat_Id) VALUES(%s, %s) RETURNING Id;', (username, chat_id))
            self.connection.commit()
            return User(self.db.fetchone()[0], username, chat_id)
        else:
            print_DB_unreachable(self.db_name)
            return None

    def removeUser(self, chat_id):
        if self.existDB():
            print(intro + self.db_name + '...Rimuozione utente' + end)
            uid = str(self.getuserId_fromChatId(chat_id))
            self.cleanCursor()
            self.db.execute('DELETE FROM Prodotti WHERE Id = %s;', (uid,))
            self.connection.commit()
            return True
        else:
            print(terminalColors.FAIL + '[Error]-[Database]: ' + self.db_name + ' not found' + end)
            return False

    def addProduct(self, name, price, qt):
        if self.existDB():
            print(intro + self.db_name + '...Aggiunta prodotto' + end)
            self.cleanCursor()
            self.db.execute('INSERT INTO Prodotti(Name, Price, Quantity) VALUES(%s, %s, %s) RETURNING Id;',
                            (name, price, qt))
            self.connection.commit()
            return Product(self.db.fetchone()[0], name, price, qt)
        else:
            print(terminalColors.FAIL + '[Error]-[Database]: ' + self.db_name + ' not found' + end)
            return None

    def removeProduct(self, product_id):
        if self.existDB():
            print(intro + self.db_name + '...Rimuovi prodotto' + end)
            self.cleanCursor()
            self.db.execute('DELETE FROM Prodotti WHERE Id = %s;', (product_id,))
            self.connection.commit()
            return True
        else:
            print(terminalColors.FAIL + '[Error]-[Database]: ' + self.db_name + ' not found' + end)
            return False

    def modifyQuantity(self, product_id, qt):
        if self.existDB():
            print(intro + self.db_name + '...Modifica quantità' + end)
            self.cleanCursor()
            self.db.execute('UPDATE Prodotti SET Quantity = %s WHERE Id = %s;', (qt, product_id))
            self.connection.commit()
            return True
        else:
            print(terminalColors.FAIL + '[Error]-[Database]: ' + self.db_name + ' not found' + end)
            return None

    def addTransaction(self, chat_id, product_id, qt):
        if self.existDB():
            d = datetime.date.today()
            uid = self.getuserId_fromChatId(chat_id)
            print(intro + self.db_name + '...Aggiunta transazione' + end)
            self.cleanCursor()
            self.db.execute('SELECT Quantity FROM Prodotti WHERE Id = %s', (product_id,))
            lastQuantity = int(self.db.fetchone()[0])

            if lastQuantity == 0:
                # Eccezione
                raise Exception("Acquisto non possibile")

            if lastQuantity - qt >= 0:
                # Ci sono ancora, aggiorno semplicemente
                self.cleanCursor()
                self.db.execute(
                    'INSERT INTO User_Prodotti(User_Id, Prodotto_Id, Data, Quantity) VALUES(%s, %s, %s, %s);',
                    (uid, product_id, d, qt))
                self.connection.commit()
                self.modifyQuantity(product_id, lastQuantity - qt)
            else:
                # Prodotto è finit, impsoto la quantità a 0
                self.modifyQuantity(product_id, 0)
            return User_Prodotti(self.db.lastrowid, uid, product_id, d, qt)
        else:
            print(terminalColors.FAIL + '[Error]-[Database]: ' + ' not found' + end)
            return None

    def removeTransaction(self, transaction_id):
        if self.existDB():
            print(intro + self.db_name + '...Rimozione transazione' + end)
            self.cleanCursor()
            self.db.execute('DELETE FROM User_Prodotti WHERE Id = %s;', (transaction_id,))
            self.connection.commit()
            return True
        else:
            print(terminalColors.FAIL + '[Error]-[Database]: ' + ' not found' + end)
            return False

    def getUserId(self, username):
        if self.existDB():
            print(intro + self.db_name + '...getUserId' + end)
            self.cleanCursor()
            self.db.execute('SELECT Id FROM Users WHERE Username = %s', (username,))
            return int(self.db.fetchone()[0])
        else:
            print(terminalColors.FAIL + '[Error]-[Database]: ' + ' not found' + end)
            return None

    def getuserId_fromChatId(self, chat_id):
        if self.existDB():
            print(intro + self.db_name + '...getUserId_fromChatId' + end)
            self.cleanCursor()
            self.db.execute('SELECT Id FROM users WHERE Chat_Id = %s', (chat_id,))
            query = self.db.fetchone()
            if query is not None:
                return query[0]
            else:
                return None
        else:
            print(terminalColors.FAIL + '[Error]-[Database]: ' + ' not found' + end)
            return None

    def getUsername_fromChatId(self, chat_id):
        if self.existDB():
            print(intro + self.db_name + '...getUsername_fromChatId' + end)
            self.cleanCursor()
            self.db.execute('SELECT Username FROM Users WHERE Chat_Id = %s', (chat_id,))
            query = self.db.fetchone()
            if query is not None:
                return query[0]
            else:
                return None
        else:
            print(terminalColors.FAIL + '[Error]-[Database]: ' + ' not found' + end)
            return None

    def getAllProduct(self):
        if self.existDB():
            prodotti = []
            print(intro + self.db_name + '...getAllProduct' + end)
            self.cleanCursor()
            self.db.execute('SELECT * FROM Prodotti')
            query = self.db.fetchall()
            for el in query:
                prodotti.append(Product(el[0], el[1], el[2], el[3]))
            return prodotti
        else:
            print(terminalColors.FAIL + '[Error]-[Database]: ' + ' not found' + end)
            return None

    def getAllChatIds(self):
        if self.existDB():
            chat_ids = []
            print(intro + self.db_name + '...getAllChatIds' + end)
            self.cleanCursor()
            self.db.execute('SELECT Chat_Id FROM Users')
            query = self.db.fetchall()
            for el in query:
                chat_ids.append(el[0])
            return chat_ids
        else:
            print(terminalColors.FAIL + '[Error]-[Database]: ' + ' not found' + end)
            return None

    def getAllAcquisti(self, chat_id):
        if self.existDB():
            acquisti = []
            uid = self.getuserId_fromChatId(chat_id)
            print(intro + self.db_name + '...getAllAcquisti' + end)
            self.cleanCursor()
            self.db.execute('SELECT * FROM User_Prodotti WHERE User_Id = %s', (uid,))
            query = self.db.fetchall()
            for el in query:
                acquisti.append(User_Prodotti(el[0], el[1], el[2], el[3], el[4]))
            return acquisti
        else:
            print(terminalColors.FAIL + '[Error]-[Database]: ' + ' not found' + end)
            return None

    def getAcquistiIn(self, chat_id, data_inizio, data_fine):
        if self.existDB():
            acquisti = []
            uid = self.getuserId_fromChatId(chat_id)
            print(intro + self.db_name + '...getAcquistiIn' + end)
            self.cleanCursor()
            self.db.execute('SELECT * FROM User_Prodotti WHERE User_Id = %s AND Data >= %s AND Data <= %s',
                            (uid, data_inizio, data_fine))
            query = self.db.fetchall()
            for el in query:
                acquisti.append(User_Prodotti(el[0], el[1], el[2], el[3], el[4]))
            return acquisti
        else:
            print(terminalColors.FAIL + '[Error]-[Database]: ' + ' not found' + end)
            return None

    def getAllDebits(self):
        if self.existDB():
            acquisti = []
            print(intro + self.db_name + '...getAllAcquisti' + end)
            self.cleanCursor()
            self.db.execute('SELECT * FROM User_Prodotti')
            query = self.db.fetchall()
            for el in query:
                acquisti.append(User_Prodotti(el[0], el[1], el[2], el[3], el[4]))
            return acquisti
        else:
            print(terminalColors.FAIL + '[Error]-[Database]: ' + ' not found' + end)
            return None

    def getAllusers(self):
        if self.existDB():
            utenti = []
            print(intro + self.db_name + '...getAcquistiIn' + end)
            self.cleanCursor()
            self.db.execute('SELECT * FROM Users')
            query = self.db.fetchall()
            for el in query:
                utenti.append(User(el[0], el[1], el[2]))
            return utenti
        else:
            print(terminalColors.FAIL + '[Error]-[Database]: ' + ' not found' + end)
            return None

    def dropAllTables(self):
        if self.existDB():
            print(terminalColors.WARNING + '[Database]: ' + '... Dropping tables' + end)
            self.cleanCursor()
            self.db.execute('DROP TABLE IF EXISTS user_prodotti, prodotti, users, debits,  CASCADE')
            self.connection.commit()
            self.db.execute(init_db)
            self.connection.commit()
            print(intro + self.db_name + ' initialization' + end)
            return True
        else:
            print_DB_unreachable(self.db_name)
            return False

    def activateActivator(self):
        if self.existDB():
            print(intro + self.db_name + '...activateActivator' + end)
            self.cleanCursor()
            self.db.execute('UPDATE Activator SET Activator = 1')
            self.connection.commit()
        else:
            print(intro + self.db_name + ' not found' + end)

    def deactivateActivator(self):
        if self.existDB():
            print(intro + self.db_name + '...deactivateActivator' + end)
            self.cleanCursor()
            self.db.execute('UPDATE Activator SET Activator = 0')
            self.connection.commit()
        else:
            print(intro + self.db_name + ' not found' + end)

    def checkActivator(self):
        if self.existDB():
            print(intro + self.db_name + '...checkActivator' + end)

            self.cleanCursor()
            self.db.execute('SELECT * FROM Activator')
            if len(self.db.fetchall()) == 0:
                print(intro + self.db_name + '...createActivatorRow' + end)
                self.db.execute('INSERT INTO Activator(activator) VALUES(0, 1)')
                self.connection.commit()

            self.db.execute('SELECT Activator FROM Activator')
            if self.db.fetchone()[0]:
                print(intro + self.db_name + ' activator activated' + end)
                print('Done')
                return True
            print('Done')
            return False
        else:
            print(intro + self.db_name + ' not found' + end)
            print(intro + self.db_name + ' initializing activator' + end)
            self.deactivateActivator()
            return False

    def checkTransaction_forProducts(self, product_id):
        if self.existDB():
            print(intro + self.db_name + "...checkTransaction_forProducts" + end)
            self.cleanCursor()
            self.db.execute('SELECT * FROM User_Prodotti WHERE Prodotto_Id = %s;', (product_id,))

            if len(self.db.fetchall()) != 0:
                print(intro + self.db_name + "Prodotto non eliminabile, transazioni correlate" + end)
                return False
            else:
                print(intro + self.db_name + "Prodotto eliminabile" + end)
                return True

    def activateBackup(self):
        if self.existDB():
            print(intro + self.db_name + self.path + '...activateBackup' + end)
            self.cleanCursor()
            self.db.execute('UPDATE Backup SET Backup = 1')
            self.connection.commit()
        else:
            print(intro + self.db_name + 'not found' + end)

    def deactivateBackup(self):
        if self.existDB():
            print(intro + self.db_name + '...deactivateBackup' + end)
            self.cleanCursor()
            self.db.execute('UPDATE Backup SET Backup = 0')
            self.connection.commit()
        else:
            print(intro + self.db_name + 'not found' + end)

    def checkBackup(self):
        if self.existDB():
            print(intro + self.db_name + '...checkBackup' + end)
            self.cleanCursor()
            self.db.execute('SELECT * FROM Backup')
            if len(self.db.fetchall()) == 0:
                print(intro + self.db_name + '...createBackupRow' + end)
                self.db.execute('INSERT INTO Backup(backup) VALUES(1)')
                self.connection.commit()

            self.db.execute('SELECT Backup FROM Backup')
            if self.db.fetchone()[0]:
                print(intro + self.db_name + ' backup activated' + end)
                print('Done')
                return True
            print('Done')
            return False
        else:
            print(intro + self.db_name + ' not found' + end)
            print(intro + self.db_name + ' initializing backup' + end)
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
            print(terminalColors.FAIL + '[Error]-[Database]: ' + ' not found' + end)
            return None

    def getProductName_fromId(self, product_id):
        if self.existDB():
            print(intro + self.db_name + '...getProductName_fromId' + end)
            self.cleanCursor()
            self.db.execute('SELECT Name FROM Prodotti WHERE Id=%s', (product_id,))
            return self.db.fetchone()[0]
        else:
            print(terminalColors.FAIL + '[Error]-[Database]: ' + ' not found' + end)
            return None

    def renameProduct_fromId(self, product_id, newname):
        if self.existDB():
            print(intro + self.db_name + '...renameProduct_fromId' + end)
            self.cleanCursor()
            self.db.execute('UPDATE Prodotti SET Name = %s WHERE Id = %s;', (newname, product_id))
            self.connection.commit()
        else:
            print(terminalColors.FAIL + '[Error]-[Database]: ' + ' not found' + end)
            return None

    def change_username(self, chat_id, new_username):
        if self.existDB():
            print(intro + self.db_name + '...change_username' + end)
            self.cleanCursor()
            self.db.execute('UPDATE Users SET Username = %s WHERE Chat_Id = %s', (new_username, chat_id))
            self.connection.commit()
            return True
        else:
            print(terminalColors.FAIL + '[Error]-[Database]: ' + ' not found' + end)
            return False

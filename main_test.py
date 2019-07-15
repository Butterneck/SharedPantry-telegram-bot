from db_connection import *
import os
import datetime

os.system("rm dispensa.db")

db_manager = DB_Connection()
db_manager.addUser("Marco", 1)
db_manager.addUser("Filippo", 2)

db_manager.addProduct("Caramelle", 5.0, 10)
db_manager.addProduct("Birra", 2.25, 20)

db_manager.addTransaction(1, int(db_manager.getAllProduct()[1].id), 1)
db_manager.addTransaction(1, int(db_manager.getAllProduct()[0].id), 2)
db_manager.addTransaction(2, int(db_manager.getAllProduct()[1].id), 1)
db_manager.addTransaction(1, int(db_manager.getAllProduct()[0].id), 3)
db_manager.addTransaction(2, int(db_manager.getAllProduct()[1].id), 1)
db_manager.addTransaction(1, int(db_manager.getAllProduct()[0].id), 2)

for el in db_manager.getAcquistiIn(1, datetime.date.today()-datetime.timedelta(3600), datetime.date.today()+datetime.timedelta(3600)):
    print(el.date, el.quantity, el.user_id, el.user_id)


#print(db_manager.getUserId("Filippo"))

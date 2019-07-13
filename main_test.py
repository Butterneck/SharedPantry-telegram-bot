from db_connection import *
import os

#os.system("rm dispensa.db")

db_manager = DB_Connection()
db_manager.addUser("Marco")
db_manager.addUser("Filippo")

db_manager.addProduct("Caramelle", 5.0, 10)
db_manager.addProduct("Birra", 2.25, 20)

print(db_manager.getAllProduct()[1].quantity)
db_manager.addTransaction(db_manager.getUserId("Marco"), int(db_manager.getAllProduct()[1].id), 2)
print(db_manager.getAllProduct()[1].name)
print(db_manager.getAllProduct()[1].quantity)


#print(db_manager.getUserId("Filippo"))

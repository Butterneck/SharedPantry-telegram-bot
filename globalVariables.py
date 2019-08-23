from db_connection_postgresql import *
import os
from Utils import terminalColors


global DB_URL_FOR_TEST
DB_URL_FOR_TEST= "postgres://ixiqvhfvwxoesq:7a7c7c6514e38c66bf3c730cee009fba2f1f4b2ebe9fd92bf100c84764312ece@ec2-176-34-184-174.eu-west-1.compute.amazonaws.com:5432/dfip2e6s7bg4ik"

DB_URL = ""
if "DATABASE_URL" in os.environ:
    DB_URL = os.environ["DATABASE_URL"]
    name = "Prod_DB"
else:
    print(terminalColors.WARNING + "DATABASE_URL not found" + terminalColors.ENDC)
    DB_URL = DB_URL_FOR_TEST
    name = "Test_DB"

global db_manager
db_manager = DB_Connection(DB_URL, name)

global chat_id_list
chat_id_list = db_manager.getAllChatIds()
db_manager.cleanCursor()

global nuovoProdotto
nuovoProdotto = None

global Ciano
Ciano = 879140791 #Ciano
global Filippo
Filippo = 32345162 #Filippo
global Marco
Marco = 179624122 #Marco

global admin_id
admin_id = [Ciano, Filippo, Marco]

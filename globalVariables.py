from db_connection_postgresql import *
import os
from Utils import terminalColors


global DB_URL_FOR_TEST
DB_URL_FOR_TEST= "postgres://fyoqpbctzdznrr:7ea4944c845d3ccc13f21022dff78137d352da194781112fd101d9830e7998ee@ec2-54-75-224-168.eu-west-1.compute.amazonaws.com:5432/d2ig29ct3113ik"

DB_URL = ""
if "DATABASE_URL" in os.environ:
    DB_URL = os.environ["DATABASE_URL"]
else:
    print(terminalColors.WARNING + "DATABASE_URL not found" + terminalColors.ENDC)
    DB_URL = DB_URL_FOR_TEST

global db_manager
db_manager = DB_Connection(DB_URL)


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

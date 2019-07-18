from db_connection_postgresql import *
import os
from Utils import terminalColors

DB_URL = ""
if "DATABASE_URL" in os.environ:
    DB_URL = os.environ["DATABASE_URL"]
else:
    print(terminalColors.WARNING + "DATABASE_URL not found" + terminalColors.ENDC)
    DB_URL = "postgres://kztdqvcvabikuw:558e67b9ac1b55d22d94a8790b5bde3918d69e89e20f136cf89e25fdbc8d39e4@ec2-54-220-0-91.eu-west-1.compute.amazonaws.com:5432/d1q4vs74un4gp1"

global db_manager
db_manager = DB_Connection(DB_URL)

global db_manager_for_test
db_manager_for_test = DB_Connection(DB_URL="postgres://kztdqvcvabikuw:558e67b9ac1b55d22d94a8790b5bde3918d69e89e20f136cf89e25fdbc8d39e4@ec2-54-220-0-91.eu-west-1.compute.amazonaws.com:5432/d1q4vs74un4gp1")

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

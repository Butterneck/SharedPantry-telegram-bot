from db_connection_postgresql import *

DB_URL = os.environ['DATABASE_URL']
global db_manager
db_manager = DB_Connection(DB_URL)

global db_manager_for_test
db_manager_for_test = DB_Connection(DB_URL="postgres://kztdqvcvabikuw:558e67b9ac1b55d22d94a8790b5bde3918d69e89e20f136cf89e25fdbc8d39e4@ec2-54-220-0-91.eu-west-1.compute.amazonaws.com:5432/d1q4vs74un4gp1")

global nuovoProdotto
nuovoProdotto = None

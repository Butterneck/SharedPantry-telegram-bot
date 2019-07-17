from db_connection_postgresql import *

DB_URL = os.environ['DATABASE_URL']
global db_manager
db_manager = DB_Connection(DB_URL)

global db_manager_for_test
db_manager_for_test = DB_Connection(DB_URL="postgres://eyicwwxwnxuxou:675f943b8955a12022eab26b184c193d3c1219c4999688d899cfb3687f33e1b4@ec2-54-217-234-157.eu-west-1.compute.amazonaws.com:5432/df8fia9ccanh45")

global nuovoProdotto
nuovoProdotto = None

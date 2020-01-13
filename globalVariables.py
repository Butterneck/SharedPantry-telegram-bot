from db_connection_postgresql import *
import os
from Utils import terminalColors
from Utils import Mese



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
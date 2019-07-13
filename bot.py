import telegram
import logging
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

from db_connection import *

# Funzioni ausiliarie
from gestisci_ordine import lista, button
from contabilita import conto
from gestisci_dispensa import aggiungi_prodotto, rimuovi_prodotto


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


db_manager = DB_Connection()

def start(bot, update):
    if (int(update.message.chat_id) not in db_manager.getAllChatIds()) :
        update.message.reply_text("Benvenuto, usa il comando /prendi per selezionare cosa hai preso dalla dispensa")
        user = update.message.from_user
        if (user.first_name):
            u = db_manager.addUser(user.first_name, update.message.chat_id)
        else:
            u = db_manager.addUser(user.username, update.message.chat_id)
        print(u.id, '\t', u.nome, '\t', u.chat_id)
    else:
        update.message.reply_text("Bentornato, usa il comando /prendi per selezionare cosa hai preso dalla dispensa")

def main():
    TOKEN = "757571867:AAHrPE1iyZ5FrWoH412U9Ubq6sO-tFA29jM"
    updater = Updater(TOKEN)
    bot = telegram.Bot(TOKEN)


    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('prendi', lista))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(CommandHandler('conto', conto))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

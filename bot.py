import telegram
import logging
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters, RegexHandler


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

NOME, PREZZO, QUANTITA = range(3)

# Variabili Globali
import globalVariables as gv


# Funzioni ausiliarie
from gestisci_ordine import lista, button
from contabilita import conto

def aggiungi_prodotto(bot, update):
    update.message.reply_text("Ok, dimmi il nome del prodotto che vuoi aggiungere")
    return NOME

def aggiungi_nome(bot, update, user_data):
    nome = update.message.text
    user_data['nome'] = nome
    update.message.reply_text("Benissimo, ora dimmi il prezzo di " + nome)
    return PREZZO


def aggiungi_prezzo(bot, update, user_data):
    prezzo = update.message.text
    user_data['prezzo'] = prezzo
    update.message.reply_text("Benissimo, ora dimmi quanti " + user_data['nome'] + " ci sono")
    return QUANTITA


def aggiungi_quantita(bot, update, user_data):
    qt = update.message.text
    update.message.reply_text("Ottimo, " + user_data['nome'] + " aggiunto alla dispensa")
    gv.db_manager.addProduct(user_data['nome'], user_data['prezzo'], qt)
    update.message.reply_text("Ok, dimmi il nome del prodotto che vuoi aggiungere")
    user_data.clear()
    return NOME

def done(bot, update, user_data):
    user_data.clear()
    return ConversationHandler.END


def start(bot, update):
    if (int(update.message.chat_id) not in gv.db_manager.getAllChatIds()) :
        update.message.reply_text("Benvenuto, usa il comando /prendi per selezionare cosa hai preso dalla dispensa")
        user = update.message.from_user
        if (user.first_name):
            u = gv.db_manager.addUser(user.first_name, update.message.chat_id)
        else:
            u = gv.db_manager.addUser(user.username, update.message.chat_id)
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
    dp.add_handler(CallbackQueryHandler(button, pass_chat_data=True))
    dp.add_handler(CommandHandler('conto', conto))


    conv_handler = ConversationHandler(
        entry_points = [CommandHandler('aggiungi', aggiungi_prodotto)],

        states = {
            NOME: [MessageHandler(Filters.text, aggiungi_nome, pass_user_data=True)],
            PREZZO: [MessageHandler(Filters.text, aggiungi_prezzo, pass_user_data=True)],
            QUANTITA: [MessageHandler(Filters.text, aggiungi_quantita, pass_user_data=True)]
        },

        fallbacks=[CommandHandler('fatto', done, pass_user_data=True)]
    )

    dp.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

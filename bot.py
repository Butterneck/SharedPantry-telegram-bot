import telegram
import logging
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters, RegexHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from emoji import emojize
import os
from CheckActivatorThread import CheckActivatorThread
from CheckBackupThread import CheckBackupThread
from Utils import terminalColors


lock = emojize(":lock:", use_aliases=True)
unlock = emojize(":unlock:", use_aliases=True)
divieto = emojize(":no_entry_sign:", use_aliases=True)
yum = emojize(":yum:", use_aliases=True)


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

AUTH = range(1)

AGGIORNA_SELEZIONE, AGGIORNA_QUANTITA, AGGIORNA_NOME, NOME, PREZZO, QUANTITA= range(6)

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
    if nome is None or nome == "":
        update.message.reply_text("Nome non valido, per favore reinseriscilo")
        return NOME

    if nome == "annulla":
        update.message.reply_text("Aggiunta nuovo prodotto annullata correttamente")
        return aggiorna_dispensa(bot, update, user_data)

    user_data['nome'] = nome
    update.message.reply_text("Benissimo, ora dimmi il prezzo di " + nome)
    return PREZZO


def aggiungi_prezzo(bot, update, user_data):
    prezzo = update.message.text
    print(prezzo)

    if prezzo == "annulla":
        update.message.reply_text("Aggiunta nuovo prodotto annullata correttamente")
        return aggiorna_dispensa(bot, update, user_data)

    if prezzo is None or not prezzo.replace('.', '', 1).replace(',', '', 1).isdigit():
        update.message.reply_text("Prezzo non valido, per favore reinseriscilo")
        return PREZZO

    if ',' in prezzo:
        prezzo = prezzo.replace(',', '.')

    user_data['prezzo'] = prezzo
    update.message.reply_text("Benissimo, ora dimmi quanti " + user_data['nome'] + " ci sono")
    return QUANTITA


def aggiungi_quantita(bot, update, user_data):
    qt = update.message.text

    if qt == "annulla":
        update.message.reply_text("Aggiunta nuovo prodotto annullata correttamente")
        return aggiorna_dispensa(bot, update, user_data)

    if qt is None or not qt.isdigit():
        update.message.reply_text("Quantità non valida, per favore reinseriscilo")
        return QUANTITA

    update.message.reply_text("Ottimo, " + user_data['nome'] + " aggiunto alla dispensa")
    gv.db_manager.addProduct(user_data['nome'], user_data['prezzo'], qt)
    user_data.clear()
    return aggiorna_dispensa(bot, update, user_data)

def done(bot, update, user_data):
    user_data.clear()
    update.message.reply_text("Operazione annullata correttamente")
    return ConversationHandler.END


def aggiorna_dispensa(bot, update, user_data):
    if update.message:
        user_data['chat_id'] = update.message.chat_id
        if int(update.message.chat_id) not in gv.admin_id:
            return ConversationHandler.END

    products = gv.db_manager.getAllProduct()
    products.sort(key=lambda p: p.name)
    keyboard = []

    while len(products) > 0:
        row = []
        product = products.pop(0)
        nome = product.name + ": " + str(product.quantity)
        if len(nome) > 19:
            # Row with one product
            row.append(InlineKeyboardButton(nome, callback_data=product.id))
        else:
            # Row with two products
            row.append(InlineKeyboardButton(nome, callback_data=product.id))
            if len(products) > 1: # Sarebbe >= con solo il > l'ultima riga viene sempre singola (Non cambio perche' mi piace di piu' cosi)
                product2 = products.pop(0)
                nome2 = product2.name + ": " + str(product2.quantity)
                if len(nome2) <= 19:
                    # Il nome del prodotto ha una lunghezza accettabile
                    row.append(InlineKeyboardButton(nome2, callback_data=product2.id))
                else:
                    # Il nome del prodotto non ha una lunghezza accettabile => lo reinserisco in cima
                    products.insert(0, product2)

        keyboard.append(row)

    keyboard.append([InlineKeyboardButton("aggiungi", callback_data='aggiungi'),InlineKeyboardButton("Termina", callback_data='termina')])

    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.send_message(chat_id=user_data['chat_id'], text="Ok, seleziona il prodotto da aggionare", reply_markup=reply_markup)
    return AGGIORNA_SELEZIONE


def aggiornaProdottiButton(bot, update, user_data, chat_data):
    data = update.callback_query
    if data.data == 'aggiungi':
        data.edit_message_text(text="Dimmi il nome del prodotto che vuoi aggiungere")
        return NOME
    elif data.data == 'termina':
        data.edit_message_text(text="Operazione terminata")
        return ConversationHandler.END
    elif data.data == 'edit_nome':
        product_name = gv.db_manager.getProductName_fromId(user_data['product_id'])
        data.edit_message_text(text="Modalita' cambio nome:\nDimmi il nuovo nome per %s" % product_name)
        return AGGIORNA_NOME
    elif data.data == 'edit_qt':
        product_name = gv.db_manager.getProductName_fromId(user_data['product_id'])
        data.edit_message_text(text="Modalita' aggiornamento quantita':\nDimmi quanti elementi vuoi aggiungere a %s" % product_name)
        return AGGIORNA_QUANTITA
    elif data.data == 'edit_annulla':
        product_name = gv.db_manager.getProductName_fromId(user_data['product_id'])
        data.edit_message_text(text="Aggiornamento di %s annullato con successo" % product_name)
        return aggiorna_dispensa(bot, update, user_data)
    elif data.data == 'remove_product':
        product_name = gv.db_manager.getProductName_fromId(user_data['product_id'])
        # Magari aggiungere una conferma
        if gv.db_manager.checkTransaction_forProducts(user_data['product_id']):
            gv.db_manager.removeProduct(user_data['product_id'])
            data.edit_message_text(text="Eliminazione %s avvenuta con successo" % product_name)
        else:
            data.edit_message_text(text="%s non eliminabile, ci sono delle transazioni collegate" % product_name)
        return aggiorna_dispensa(bot, update, user_data)
    else:
        user_data['product_id'] = data.data
        product_name = gv.db_manager.getProductName_fromId(user_data['product_id'])
        keyboard = [[InlineKeyboardButton("Nome", callback_data='edit_nome'), InlineKeyboardButton("Quantita'", callback_data='edit_qt')],
                                [InlineKeyboardButton("Elimina", callback_data='remove_product'), InlineKeyboardButton("Annulla", callback_data='edit_annulla')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        data.edit_message_text(text = "%s selezionato, cosa vuoi modificare?" % product_name, reply_markup=reply_markup)
        return AGGIORNA_SELEZIONE


def aggiorna_quantita(bot, update, user_data):
    products = gv.db_manager.getAllProduct()
    currentQt = list(filter(lambda product : product.id == int(user_data['product_id']), products))[0].quantity

    #Update quantity
    qtToAdd = int(update.message.text)
    gv.db_manager.modifyQuantity(user_data['product_id'], currentQt + qtToAdd)
    update.message.reply_text("Ottimo, aggiornato!")
    return aggiorna_dispensa(bot, update, user_data)


def aggiorna_nome(bot, update, user_data):
    old_name = gv.db_manager.getProductName_fromId(user_data['product_id'])
    new_name = update.message.text
    gv.db_manager.renameProduct_fromId(user_data['product_id'], new_name)
    update.message.reply_text("Nome cambiato da %s a %s" % (old_name, new_name))
    return aggiorna_dispensa(bot, update, user_data)


def start(bot, update):
    if (int(update.message.chat_id) not in gv.db_manager.getAllChatIds()) :
        update.message.reply_text("Benvenuto, inserisci la password " + lock + " per accedere")
        return AUTH
    else:
        update.message.reply_text("Bentornato, usa il comando /prendi per selezionare cosa hai preso dalla dispensa")
        return ConversationHandler.END


def auth(bot, update, user_data):
    if (update.message.text == "Bordello") :
        gv.chat_id_list.append(str(update.message.chat_id))
        update.message.reply_text("taverna sbloccata " + unlock + "Benvenuto, usa il comando /prendi per selezionare cosa hai preso dalla dispensa" + yum)
        user = update.message.from_user
        if user.first_name and user.last_name:
            u = gv.db_manager.addUser(user.first_name + " " + user.last_name, update.message.chat_id)
        elif user.first_name:
            u = gv.db_manager.addUser(user.first_name + " senza congome" , update.message.chat_id)
        elif user.last_name:
            u = gv.db_manager.addUser("senza nome" + " " + user.last_name, update.message.chat_id)
        elif user.username:
            u = gv.db_manager.addUser(user.username, update.message.chat_id)
        else:
            u = gv.db_manager.addUser("Sconosciuto", update.message.chat_id)
        return ConversationHandler.END
    else:
        update.message.reply_text("Password errata" + divieto + " digita /start per riprovare")
        return ConversationHandler.END


def help(bot, update):
    if update.message.chat_id not in gv.chat_id_list:
        print("Utente " + str(update.message.chat_id) + " non registrato")
        return

    help_message = ("Ciao, ecco i comandi che puoi usare con me:\n\n"
                                    "/prendi - Permette di ottenere la lista di prodotti attualmente disponibili all'acquisto in taverna. Affianco ad ogni prodotto "
                                    "e' scritto il relativo prezzo. Per acquistare un prodotto premi semplicemente sopra di esso, questo verra' aggiunto al tuo conto mensile.\n\n"
                                    "/conto - Permette di vedere il resoconto delle proprie spese in taverna nel corso dell'ultimo mese. "
                                    "Il resoconto permette di vedere i prodotti acquistati e la relativa quantita', oltre che mostrare una pratica somma comprendente tutti "
                                    "gli acquisti effettuati.\n\n"
                                    "/help - Mostra questo messaggio di aiuto\n\n"
                                    "Ricorda: al termine di ogni mese verra' calcolato il debito accumulato durante il mese appena concluso e, se"
                                    " il conto dovesse risultare non nullo, riceverai un messaggio contentente il tuo debito accumulato. Allo stesso tempo verra' notificata a Ciano l'entita' del"
                                    " tuo debito.\n\n"
                                    "Buoni acquisti in taverna")

    update.message.reply_text(help_message)

def main():

    TOKEN = "757571867:AAHrPE1iyZ5FrWoH412U9Ubq6sO-tFA29jM"
    updater = Updater(TOKEN)
    PORT = int(os.environ.get('PORT', '8443'))
    bot = telegram.Bot(TOKEN)

    # Inizializzo il thread per il check del contomensile
    checkActivator = CheckActivatorThread(bot)
    checkActivator.start()

    # Inizializzo il thread per il check del backup
    checkBackup = CheckBackupThread()
    checkBackup.start()

    dp = updater.dispatcher


    conv_handlerStart = ConversationHandler(
        entry_points = [CommandHandler('start', start)],

        states = {
            AUTH: [MessageHandler(Filters.text, auth, pass_user_data=True)]
        },

        fallbacks = [CommandHandler('fatto', done, pass_user_data=True)]
    )


    conv_handlerAggiornaDispensa = ConversationHandler(
        entry_points = [CommandHandler('gestisci', aggiorna_dispensa, pass_user_data=True)],

        states = {
            AGGIORNA_SELEZIONE: [CallbackQueryHandler(aggiornaProdottiButton, pass_chat_data=True, pass_user_data=True)],
            AGGIORNA_QUANTITA: [MessageHandler(Filters.text, aggiorna_quantita, pass_user_data=True)],
            AGGIORNA_NOME: [MessageHandler(Filters.text, aggiorna_nome, pass_user_data=True)],
            NOME: [MessageHandler(Filters.text, aggiungi_nome, pass_user_data=True)],
            PREZZO: [MessageHandler(Filters.text, aggiungi_prezzo, pass_user_data=True)],
            QUANTITA: [MessageHandler(Filters.text, aggiungi_quantita, pass_user_data=True)]
        },

        fallbacks = [CommandHandler('fatto', done, pass_user_data=True)]
    )

    dp.add_handler(conv_handlerStart)
    dp.add_handler(conv_handlerAggiornaDispensa)
    dp.add_handler(CommandHandler('prendi', lista))
    dp.add_handler(CallbackQueryHandler(button, pass_chat_data=True))
    dp.add_handler(CommandHandler('conto', conto))
    dp.add_handler(CommandHandler('help', help))


    if "HEROKU" in os.environ:
        print(terminalColors.WARNING + 'Starting Webhook' + terminalColors.ENDC)
        updater.start_webhook(listen='0.0.0.0',
                                                port=PORT,
                                                url_path=TOKEN)
        updater.bot.set_webhook("https://cianobot.herokuapp.com/" + TOKEN)
    else:
        print(terminalColors.WARNING + 'Starting Polling' + terminalColors.ENDC)
        updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

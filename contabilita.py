import datetime
from Utils import removeDuplicateInAcquisti, getNumAcquisti
from functools import reduce
import globalVariables as gv

def conto(bot, update):
    """Informa l'utente del suo debito con ciano"""
    acquisti = gv.db_manager.getAcquistiIn(update.message.chat_id, datetime.date.today().replace(day=1), datetime.date.today())

    allProducts = gv.db_manager.getAllProduct()

    totalPrice = 0

    message = "Questo mese hai acquistato dalla taverna le seguenti cose: \n"

    acquistiSingoli = removeDuplicateInAcquisti(acquisti)
    for acquistoSingolo in acquistiSingoli:
        qt = getNumAcquisti(acquistoSingolo, acquisti)
        product = list(filter(lambda el : el.id == acquistoSingolo.product_id, allProducts))
        partialPrice = product[0].price * qt
        message = message + product[0].name + " x" + str(qt) + " = €" + str(partialPrice) + "\n"
        totalPrice += partialPrice

    if totalPrice:
        message = message + "Totale debito: $" + str(totalPrice)
        update.message.reply_text(message)
    else:
        update.message.reply_text("Non hai ancora acquistato niente dalla taverna questo mese")


def debitoMensile(bot):
    chat_ids = gv.db_manager.getAllChatIds()
    messaggio_di_debito = "Ecco chi ha acquistato dalla taverna questo mese:\n"

    for chat_id in chat_ids:
        acquisti = gv.db_manager.getAcquistiIn(chat_id, datetime.date.today().replace(day=1), datetime.date.today())

        allProducts = gv.db_manager.getAllProduct()

        totalPrice = 0

        message = "Ecco il resoconto degli acquiti nella dispensa della taverna del mese appena trascorso: \n"

        acquistiSingoli = removeDuplicateInAcquisti(acquisti)
        for acquistoSingolo in acquistiSingoli:
            qt = getNumAcquisti(acquistoSingolo, acquisti)
            product = list(filter(lambda el : el.id == acquistoSingolo.product_id, allProducts))
            partialPrice = product[0].price * qt
            message = message + product[0].name + " x" + str(qt) + " = €" + str(partialPrice) + "\n"
            totalPrice += partialPrice

        if totalPrice:
            message = message + "Totale debito: $" + str(totalPrice) + "\nDovrai saldare il debito direttamente con Ciano"
            messaggio_di_debito = messaggio_di_debito + gv.db_manager.getUsername_fromChatId(chat_id) + ": $" + str(totalPrice) + "\n"

            bot.send_message(chat_id=chat_id, text=message)

    bot.send_message(chat_id=gv.Marco, text=messaggio_di_debito)
    bot.send_message(chat_id=gv.Ciano, text=messaggio_di_debito)

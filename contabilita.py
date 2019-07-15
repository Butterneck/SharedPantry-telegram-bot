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

    message = message + "Totale debito: $" + str(totalPrice)
    update.message.reply_text(message)

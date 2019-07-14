import datetime
from functools import reduce
import globalVariables as gv

def conto(bot, update):
    """Informa l'utente del suo debito con ciano"""
    acquisti = gv.db_manager.getAcquistiIn(update.message.chat_id, datetime.date.today().replace(day=1), datetime.date.today())

    allProducts = gv.db_manager.getAllProduct()

    totalPrice = 0

    message = "Questo mese hai acquistato dalla taverna le seguenti cose: \n"
    for acquisto in acquisti:
        product = list(filter(lambda el : el.id == acquisto.product_id, allProducts))
        message = message + product[0].name + " x" + str(len(product)) + " = $"
        partialPrice = product[0].price * len(product)
        totalPrice += partialPrice
        message = message + str(totalPrice) + "\n"

    message = message + "Totale debito: " + str(totalPrice)

    update.message.reply_text(message)

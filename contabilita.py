import datetime
from Utils import removeDuplicateInAcquisti, getNumAcquisti
from functools import reduce
import globalVariables as gv

def conto(bot, update):
    """Informa l'utente del suo debito con ciano"""
    if update.message.chat_id not in gv.chat_id_list:
        print("Utente " + str(update.message.chat_id) + " non registrato")
        return

    acquisti = gv.db_manager.getAcquistiIn(update.message.chat_id, datetime.date.today().replace(day=1), datetime.date.today())

    allProducts = gv.db_manager.getAllProduct()

    totalPrice = 0

    message = "Questo mese hai acquistato dalla taverna le seguenti cose: \n"

    acquistiSingoli = removeDuplicateInAcquisti(acquisti)
    for acquistoSingolo in acquistiSingoli:
        qt = int(getNumAcquisti(acquistoSingolo, acquisti))
        product = list(filter(lambda el: el.id == acquistoSingolo.product_id, allProducts))
        partialPrice = int(product[0].price * 100) * qt
        message = message + product[0].name + " x" + str(qt) + " = €" + str(partialPrice/100) + "\n"
        totalPrice += partialPrice

    if totalPrice:
        message = message + "Totale debito: $" + str(totalPrice/100)
        update.message.reply_text(message)
    else:
        update.message.reply_text("Non hai ancora acquistato niente dalla taverna questo mese")


def debitoMensile(bot):
    chat_ids = gv.db_manager.getAllChatIds()
    messaggio_di_debito = "Ecco chi ha acquistato dalla taverna questo mese:\n"

    for chat_id in chat_ids:
        # Check that it's the first day of the month
        if datetime.date.today().day != 1:
            print("Oggi non e' il primo giorno del mese, perche' si sta cercando di inviare il conto mensile?")

        mesePrecedente = gv.mesiAnno[datetime.date.today().month - 1].getMesePrecedente()
        annoMesePrecedente = datetime.date.today().year - 1 if mesePrecedente.numMese == 12 else datetime.date.today().year

        # Check anno bisestile
        if mesePrecedente.numMese == 2 and not ((annoMesePrecedente - 2000) % 4):
            mesePrecedente.numGiorni = mesePrecedente.getNumGiorni() + 1

        acquisti = gv.db_manager.getAcquistiIn(chat_id, datetime.date(annoMesePrecedente, mesePrecedente.getNumMese(), 1), datetime.date(annoMesePrecedente, mesePrecedente.getNumMese(), mesePrecedente.getNumGiorni()))

        allProducts = gv.db_manager.getAllProduct()

        totalPrice = 0

        message = "Ecco il resoconto degli acquiti nella dispensa della taverna del mese di " + mesePrecedente.nome + ": \n"

        acquistiSingoli = removeDuplicateInAcquisti(acquisti)
        for acquistoSingolo in acquistiSingoli:
            qt = getNumAcquisti(acquistoSingolo, acquisti)
            product = list(filter(lambda el: el.id == acquistoSingolo.product_id, allProducts))
            partialPrice = int(product[0].price*100) * qt
            message = message + product[0].name + " x" + str(qt) + " = €" + str(partialPrice/100) + "\n"
            totalPrice += partialPrice

        if totalPrice:
            message = message + "Totale debito: $" + str(totalPrice/100) + "\nDovrai saldare il debito direttamente con Ciano"
            messaggio_di_debito = messaggio_di_debito + gv.db_manager.getUsername_fromChatId(chat_id) + ": $" + str(totalPrice/100) + "\n"

            bot.send_message(chat_id=chat_id, text=message)

    bot.send_message(chat_id=gv.Filippo, text=messaggio_di_debito)
    bot.send_message(chat_id=gv.Marco, text=messaggio_di_debito)
    bot.send_message(chat_id=gv.Ciano, text=messaggio_di_debito)

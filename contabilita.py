import datetime
from Utils import removeDuplicateInAcquisti, getNumAcquisti
from authenticator import Authenticator
from Anno import Anno


class Wallet():

    def getConto(self, update, db_manager):
        totalPrice = 0

        allProducts = db_manager.getAllProduct()
        acquisti = db_manager.getAcquistiIn(update.message.chat_id, datetime.date.today().replace(day=1), datetime.date.today())
        acquistiSingoli = removeDuplicateInAcquisti(acquisti)

        message = "Questo mese hai acquistato dalla taverna le seguenti cose: \n"

        for acquistoSingolo in acquistiSingoli:
            qt = int(getNumAcquisti(acquistoSingolo, acquisti))
            product = list(filter(lambda el: el.id == acquistoSingolo.product_id, allProducts))
            partialPrice = int(product[0].price * 100) * qt
            message = message + product[0].name + " x" + str(qt) + " = €" + str(partialPrice/100) + "\n"
            totalPrice += partialPrice

        if totalPrice:
            message = message + "Totale debito: €" + str(totalPrice/100)
            return message
        else:
            return "Non hai acquistato niente dalla taverna questo mese"


    def sendConto(self, update, db_manager):
        """
            Informa l'utente del debito con Ciano
        """

        if not Authenticator().checkAuthentication(update):
            return

        update.message.reply_text(self.getConto(update, db_manager))


    def sendDebitoMensile(self, bot, db_manager):
        chat_ids = db_manager.getAllChatIds()
        messaggio_di_debito = "Ecco chi ha acquistato dalla taverna questo mese:\n"

        mesePrecedente = Anno().anno[datetime.date.today().month - 1].getMesePrecedente()
        annoMesePrecedente = datetime.date.today().year - 1 if mesePrecedente.numMese == 12 else datetime.date.today().year

        # Check anno bisestile
        if mesePrecedente.numMese == 2 and not ((annoMesePrecedente - 2000) % 4):
            mesePrecedente.numGiorni = mesePrecedente.getNumGiorni() + 1

        allProducts = db_manager.getAllProduct()

        for chat_id in chat_ids:
            totalPrice = 0
            message = "Ecco il resoconto degli acquisti nella dispensa dela tavernna del mese di " + mesePrecedente.nome + ": \n"
            acquisti = db_manager.getAcquistiIn(chat_id,
                                                datetime.date(annoMesePrecedente,
                                                              mesePrecedente.getNumMese(), 1),
                                                datetime.date(annoMesePrecedente,
                                                              mesePrecedente.getNumMese(),
                                                              mesePrecedente.getNumGiorni()))
            acquistiSingoli = removeDuplicateInAcquisti(acquisti)
            for acquistoSingolo in acquistiSingoli:
                qt = getNumAcquisti(acquistoSingolo, acquisti)
                product = list(filter(lambda el: el.id == acquistoSingolo.product_id, allProducts))
                partialPrice = int(product[0].price * 100) * qt
                message = message + product[0].name + " x" + str(qt) + " = €" + str(partialPrice/100) + "\n"
                totalPrice += partialPrice

            if totalPrice:
                message = message + "Totale debito: €" + str(totalPrice/100) + "\nDovrai saldare il debito direttamente con Ciano"
                messaggio_di_debito = messaggio_di_debito + db_manager.getUsername_fromChatId(chat_id) + ": €" + str(totalPrice/100) + "\n"
                bot.send_message(chat_id = chat_id, text=message)

        bot.sendMessage(chat_id=Authenticator().Filippo, text=messaggio_di_debito)
        bot.sendMessage(chat_id=Authenticator().Marco, text=messaggio_di_debito)
        bot.sendMessage(chat_id=Authenticator().Ciano, text=messaggio_di_debito)
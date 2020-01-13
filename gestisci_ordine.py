from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from authenticator import Authenticator

def lista(bot, update, db_manager):
    """Crea la tastiera personalizzata e invia il messaggio di presentazione"""
    if not Authenticator().checkAuthentication(update):
        return

    products = db_manager.getAllProduct()
    products = list(filter(lambda product: product.quantity > 0, products))
    products.sort(key=lambda p: p.name)
    keyboard = []

    while len(products) > 0:
        row = []
        product = products.pop(0)
        nome = str(product.quantity) + " - " + product.name + ": €" + str(product.price)
        if len(nome) > 19:
            #row with one product
            row.append(InlineKeyboardButton(nome, callback_data=product.id))
        else:
            #row with two products
            row.append(InlineKeyboardButton(nome, callback_data=product.id))
            if len(products) > 1: # Sarebbe >= con solo il > l'ultima riga viene sempre singola (Non cambio perche' mi piace di piu' cosi)
                #c'è almeno un altro prodotto
                product2 = products.pop(0)
                nome2 = str(product2.quantity) + " - " + product2.name + ": €" + str(product2.price)
                if len(nome2) <= 19:
                    #il nome del prodotto ha una lunghezza accettabile
                    row.append(InlineKeyboardButton(nome2, callback_data=product2.id))
                else:
                    #il nome del prodotto non ha un alunghezza accettabile => lo reiserisco in cima
                    products.insert(0, product2)

        keyboard.append(row)

    if len(keyboard):

        keyboard.append([InlineKeyboardButton("Annulla", callback_data='annullaOrdine')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text("Questo e' quello che offre la taverna, scegli responsabilmente",
                                                        reply_markup=reply_markup)
    else:
        update.message.reply_text("Al momento la taverna non ha nulla da offrirti, torna piu' tardi")


def button(bot, update, chat_data, db_manager):
    """Gestisce la callback del prodotto scelto"""
    data = update.callback_query
    if data.data == 'annullaOrdine':
        data.edit_message_text(text="Annullato correttamente")
        return
    try:
        db_manager.addTransaction(int(update.callback_query.message.chat_id), int(data.data), 1)
        data.edit_message_text(text="Ottimo, torna presto a trovarci!")
    except:
        data.edit_message_text(text="Mi spiace, arrivi tardi, e' finito")

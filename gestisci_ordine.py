from telegram import InlineKeyboardButton, InlineKeyboardMarkup

import globalVariables as gv

def lista(bot, update):
    """Crea la tastiera personalizzata e invia il messaggio di presentazione"""

    products = gv.db_manager.getAllProduct()
    products = list(filter(lambda product: product.quantity > 0, products))
    keyboard = []

    for i in range(len(products) // 3):
        row = []
        for j in range(3):
            product = products[i * 3 + j]
            nome = product.name + " : " + str(product.id)
            row.append(InlineKeyboardButton(nome, callback_data=product.id))

        keyboard.append(row)

    row = []
    for i in range(len(products) % 3):
        product = products[len(products) - i - 1]
        nome = product.name + " : " + str(product.id)
        row.append(InlineKeyboardButton(nome, callback_data=product.id))

    keyboard.append(row)

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text("Questo e' quello che offre la taverna, scegli responsabilmente",
                                                    reply_markup=reply_markup)


def button(bot, update, chat_data):
    """Gestisce la callback del prodotto scelto"""
    product = update.callback_query
    print(product.data)

    print(gv.db_manager.addTransaction(int(update.callback_query.message.chat_id), int(product.data), 1).quantity)

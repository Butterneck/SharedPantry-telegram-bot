from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def lista(bot, update):
    """Crea la tastiera personalizzata e invia il messaggio di presentazione"""
    keyboard = [[InlineKeyboardButton("Option 1 row 0", callback_data='aaa')],

                        [InlineKeyboardButton("Option 1 row 1", callback_data='bbb'),
                        InlineKeyboardButton("Option 2 row 1", callback_data='ccc')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text("Questo e' quello che offre la taverna, scegli responsabilmente",
                                                    reply_markup=reply_markup)


def button(bot, update):
    """Gestisce la callback del prodotto scelto"""
    query = update.callback_query

    query.edit_message_text(text="Selected option: {}".format(query.data))

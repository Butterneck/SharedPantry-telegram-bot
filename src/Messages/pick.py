from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from src.Auth.authenticator import Authenticator
import json
import logging

from src.Utils.BackendRequests import request, validate_response

from src.Utils.Translator import translate as _


def pick(update, context):
    if not Authenticator().checkUserExistence(update.message.chat_id):
        return

    r = request('/getAllProducts')
    if validate_response(r):
        products = json.loads(r.text)['products']
        products = list(filter(lambda product: product['quantity'] > 0, products))
        products.sort(key=lambda p: p['name'])
        keyboard = build_keyboard(products)
        if len(keyboard):
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text(_('AVAILABLE_PRODUCTS', update.message.chat_id), reply_markup=reply_markup)
        else:
            update.message.reply_text(_('NO_AVAILABLE_PRODUCTS', update.message.chat_id))
    else:
        return


def build_keyboard(products):
    keyboard = []
    while len(products) > 0:
        row = []
        product = products.pop(0)
        name = str(product['quantity']) + " - " + product['name'] + ": €" + str(product['price'])
        if len(name) > 19:
            row.append(InlineKeyboardButton(name, callback_data=product['id']))
        else:
            row.append(InlineKeyboardButton(name, callback_data=product['id']))
            if len(products) > 1:
                product2 = products.pop(0)
                name2 = str(product2['quantity']) + " - " + product2['name'] + ": €" + str(product2['price'])
                if len(name2) <= 19:
                    row.append(InlineKeyboardButton(name2, callback_data=product2['id']))
                else:
                    products.insert(0, product2)

        keyboard.append(row)

    if len(keyboard):
        keyboard.append([InlineKeyboardButton('Cancel', callback_data='cancelOrder')])

    return keyboard


def button(update, context):
    data = update.callback_query
    if data.data == 'cancelOrder':
        data.edit_message_text(text=_('ORDER_CANCELLED', update.callback_query.message.chat.id))
        return
    r = request('/addTransaction', {
        'chat_id': update.callback_query.message.chat_id,
        'product_id': data.data,
        'quantity': '1'
    })
    if r.status_code == 200:
        logging.info('new transaction correctly added')
        data.edit_message_text(text=_('ORDER_COMPLETED', update.message.chat_id))
    elif r.status_code == 500:
        logging.info('new transaction failed to add')
        data.edit_message_text(text=_('FINISHED_PRODUCT', update.message.chat_id))
    else:
        logging.warning('Wrong backend token')



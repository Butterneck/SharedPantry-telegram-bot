import logging
from datetime import datetime
import json

from src.Utils.BackendRequests import request, validate_response
from src.Auth.authenticator import Authenticator


def send_bill_message(bot, update):
    if not Authenticator().checkUserExistence(update.message.chat_id):
        return
    update.message.reply_text(get_bill_message(update.message.chat_id))


def get_bill_message(chat_id):
    r = request('/getAcquistiIn', {
        'user_id': chat_id,
        'start_date': str(datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)),
        'end_date': str(datetime.now().replace(microsecond=0))
    })
    if not validate_response(r):
        return

    allTransactions = json.loads(r.text)['transactions']

    r = request('/getAllProducts')
    if not validate_response(r):
        return

    allProducts = json.loads(r.text)['products']
    singleTransaction = remove_duplicated_products_in_transactions(allTransactions)

    totalPrice = 0
    message = "This month you bought this:\n"

    for transaction in singleTransaction:
        quantity = get_frequency(transaction['product_id'], allTransactions)
        product = list(filter(lambda el: el['id'] == transaction['product_id'], allProducts))[0]
        partialPrice = int(product['price'] * 100) * quantity
        totalPrice += partialPrice
        message = message + product['name'] + ' x' + str(quantity) + '= €' + str(partialPrice/100) + '\n'

    if totalPrice:
        message = message + 'Total bill: €' + str(totalPrice/100)
        return message
    else:
        return "You did'n boy anything this month yet"



def remove_duplicated_products_in_transactions(transactions):
    retList = []
    for transaction in transactions:
        if transaction['product_id'] not in list(map(lambda el: el['product_id'], retList)):
            retList.append(transaction)
    return retList


def get_frequency(product_id, transactions):
    counter = 0
    for transaction in transactions:
        if product_id == transaction['product_id']:
            counter += 1
    return counter
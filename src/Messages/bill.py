import logging
from datetime import datetime, date
import json

from src.Utils.BackendRequests import request, validate_response
from src.Auth.authenticator import Authenticator
from src.Utils.Year import Year


def send_monthly_bill_message(bot, update):
    admin_message = "Here is who bought something this month:\n"
    previous_month = Year().year[date.today().month - 1].getPreviousMonth()
    previous_month_year = date.today().year - 1 if previous_month.monthNum == 12 else date.today().year

    # Check for leap year
    if previous_month.monthNum == 2 and not ((previous_month_year - 2000) % 4):
        previous_month.days = previous_month.getNumDays() + 1

    r = request('/getAllProducts')
    if not validate_response(r):
        return

    allProducts = json.loads(r.text)['products']
    start_date = str(date(previous_month_year, previous_month.getNumMonth(), 1))
    end_date = str(date(previous_month_year, previous_month.getNumMonth(), previous_month.getNumDays()))
    for user in json.loads(request('/getAllUsers').text)['users']:
        print(user)
        bill, totalPrice = get_bill_message(user['chat_id'], start_date, end_date, allProducts)
        if bill is not None:
            admin_message = admin_message + user['username'] + ": €" + str(totalPrice/100) + "\n"
            user_message = "Here is what you bought in previous month:\n"
            user_message += bill
            user_message += "\nYou'll have to pay admins directly"
            bot.sendMessage(chat_id=user['chat_id'], text=user_message)

    for admin in json.loads(request('/getAllAdmins').text)['admins']:
        bot.sendMessage(chat_id=admin['chat_id'], text=admin_message)


def send_bill_message(bot, update):
    if not Authenticator().checkUserExistence(update.message.chat_id):
        return
    start_date = str(datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0))
    end_date = str(datetime.now().replace(microsecond=0))
    message = "This month you bought this:\n"
    r = request('/getAllProducts')
    if not validate_response(r):
        return
    allProducts = json.loads(r.text)['products']
    bill, totalPrice = get_bill_message(update.message.chat_id, start_date, end_date, allProducts)
    if bill is None:
        message = "You did'n buy anything this month yet"
    else:
        message += bill
    update.message.reply_text(message)


def get_bill_message(chat_id, start_date, end_date, allProducts):
    bill, totalPrice = calculate_debit(allProducts, chat_id, start_date, end_date)
    if bill is not None:
        return [bill, totalPrice]
    else:
        return [None, None]


def calculate_debit(allProducts, chat_id, start_date, end_date):
    totalPrice = 0
    message = ''

    r = request('/getAcquistiIn', {
        'user_id': chat_id,
        'start_date': start_date,
        'end_date': end_date
    })
    if not validate_response(r):
        return [None, None]

    allTransactions = json.loads(r.text)['transactions']
    print(allTransactions)
    singleTransactions = remove_duplicated_products_in_transactions(allTransactions)
    for transaction in singleTransactions:
        print('transaction')
        quantity = get_frequency(transaction['product_id'], allTransactions)
        product = list(filter(lambda el: el['id'] == transaction['product_id'], allProducts))[0]
        partialPrice = int(product['price'] * 100) * quantity
        totalPrice += partialPrice
        message = message + product['name'] + ' x' + str(quantity) + '= €' + str(partialPrice/100) + '\n'

    print(totalPrice)
    if totalPrice:
        message = message + 'Total bill: €' + str(totalPrice/100)
        return [message, totalPrice]
    else:
        return [None, None]


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
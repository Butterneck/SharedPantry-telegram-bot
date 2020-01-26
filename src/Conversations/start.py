from os import environ
from telegram.ext import ConversationHandler
from emoji import emojize

import logging

from src.Utils.BackendRequests import request

from src.Auth.authenticator import Authenticator

lock = emojize(":lock:", use_aliases=True)
unlock = emojize(":unlock:", use_aliases=True)
divieto = emojize(":no_entry_sign:", use_aliases=True)


def start(bot, update):
    from bot import AUTH
    if Authenticator().checkUserExistence(update.message.chat_id):
        update.message.reply_text("Welcome back message")
        return ConversationHandler.END
    else:
        logging.warning('New user ' + str(update.message.chat_id) + ' is connecting')
        update.message.reply_text("Welcome, put your password, please")
        return AUTH


def auth(bot, update):
    if update.message.text == environ['Password']:
        update.message.reply_text("You're now logged in")
        user = update.message.from_user
        if user.first_name and user.last_name:
            username = ' '.join([user.first_name, user.last_name])
            logging.warning('New user ' + username + ' is connected')
        elif user.first_name:
            username = ' '.join([user.first_name, 'senza cognome'])
            logging.warning('New user ' + username + ' is connected')
        elif user.last_name:
            username = ' '.join([user.last_name, 'senza nome'])
            logging.warning('New user ' + username + ' is connected')
        else:
            username = 'Sconosciuto'
            logging.warning('New user ' + username + ' is connected')

        request('/addUser', {
            'chat_id': update.message.chat_id,
            'username': username
        })
    else:
        logging.info('User ' + str(update.message.chat_id) + ' put wrong password')
        update.message.reply_text("Wrong password, type /start again to retry")
        return ConversationHandler.END

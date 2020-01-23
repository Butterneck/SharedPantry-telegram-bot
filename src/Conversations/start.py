from os import environ
from telegram.ext import ConversationHandler
from emoji import emojize

from src.Utils.BackendRequests import request

from src.Auth.authenticator import Authenticator

lock = emojize(":lock:", use_aliases=True)
unlock = emojize(":unlock:", use_aliases=True)
divieto = emojize(":no_entry_sign:", use_aliases=True)


def start(bot, update):
    from refactoredBot import AUTH
    if Authenticator().checkUserExistence(update.message.chat_id):
        update.message.reply_text("Welcome back message")
        return ConversationHandler.END
    else:
        update.message.reply_text("Welcome, put your password, please")
        return AUTH


def auth(bot, update):
    if update.message.text == environ['Password']:
        update.message.reply_text("You're now logged in")
        user = update.message.from_user
        if user.first_name and user.last_name:
            request('/addUser', {
                'chat_id': update.message.chat_id,
                'username': ' '.join([user.first_name, user.last_name])
            })
        elif user.first_name:
            request('/addUser', {
                'chat_id': update.message.chat_id,
                'username': ' '.join([user.first_name, 'senza cognome'])
            })
        elif user.last_name:
            request('/addUser', {
                'chat_id': update.message.chat_id,
                'username': ' '.join([user.last_name, 'senza nome'])
            })
        else:
            request('/addUser', {
                'chat_id': update.message.chat_id,
                'username': 'Sconosciuto'
            })

    else:
        update.message.reply_text("Wrong password, type /start again to retry")
        return ConversationHandler.END

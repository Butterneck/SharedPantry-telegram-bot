import requests
import json
from os import environ
from telegram.ext import ConversationHandler
from refactoredBot import AUTH
from emoji import emojize


lock = emojize(":lock:", use_aliases=True)
unlock = emojize(":unlock:", use_aliases=True)
divieto = emojize(":no_entry_sign:", use_aliases=True)


def start(bot, update):
    user = json.loads(requests.post(
            environ['BACKEND_URL'] + '/getUserFromChatId',
            json={'token': environ['BACKEND_TOKEN']}).text)
    if user is None:
        update.message.reply_text("Welcome back message")
        return ConversationHandler.END
    else:
        update.message.reply_text("Welcome, put your password, please")
        return AUTH


def auth(bot, update):
    if (update.message.text == environ['Password']):
        update.message.reply_text("You're no logged in")
        user = update.message.from_user
        if user.first_name and user.last_name:
            requests.post(environ['BACKEND_URL'] + '/addUser',
                          json = {'token': environ['BACKEND_TOKEN'],
                                  'data': {
                                      'chat_id': update.message.chat_id,
                                      'username': ' '.join([user.first_name, user.last_name])
                                    }
                                  })
        elif user.first_name:
            requests.post(environ['BACKEND_URL'] + '/addUser',
                          json={'token': environ['BACKEND_TOKEN'],
                                'data': {
                                    'chat_id': update.message.chat_id,
                                    'username': ' '.join([user.first_name, 'senza cognome'])
                                  }
                                })
        elif user.last_name:
            requests.post(environ['BACKEND_URL'] + '/addUser',
                          json={'token': environ['BACKEND_TOKEN'],
                                'data': {
                                    'chat_id': update.message.chat_id,
                                    'username': ' '.join([user.first_name, 'senza nome'])
                                  }
                                })
        else:
            requests.post(environ['BACKEND_URL'] + '/addUser',
                          json={'token': environ['BACKEND_TOKEN'],
                                'data': {
                                    'chat_id': update.message.chat_id,
                                    'username': 'Sconosciuto'
                                  }
                                })
    else:
        update.message.reply_text("Wrong password, type /start again to retry")
        return ConversationHandler.END

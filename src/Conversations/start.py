from os import environ
from telegram.ext import ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from emoji import emojize

import logging

from src.Utils.BackendRequests import request

from src.Auth.authenticator import Authenticator

from src.Utils.Translator import translate as _

lock = emojize(":lock:", use_aliases=True)
unlock = emojize(":unlock:", use_aliases=True)
forbidden = emojize(":no_entry_sign:", use_aliases=True)
italian = emojize(':it:', use_aliases=True)
english = emojize(':uk:', use_aliases=True)


def start(update, context):
    from bot import AUTH
    if Authenticator().checkUserExistence(update.message.chat_id):
        update.message.reply_text(_('OLD_USER_WELCOME', update.message.chat_id))
        return ConversationHandler.END
    else:
        logging.warning('New user ' + str(update.message.chat_id) + ' is connecting')
        update.message.reply_text(lock + ' Welcome, put your password please')
        return AUTH


def auth(update, context):
    from bot import LANG
    if update.message.text == environ['Password']:
        user = update.message.from_user
        if user.first_name and user.last_name:
            username = ' '.join([user.first_name, user.last_name])
            logging.warning('New user ' + username + ' is connected')
        elif user.first_name:
            username = ' '.join([user.first_name, 'without surname'])
            logging.warning('New user ' + username + ' is connected')
        elif user.last_name:
            username = ' '.join([user.last_name, 'without name'])
            logging.warning('New user ' + username + ' is connected')
        else:
            username = 'Unknown'
            logging.warning('New user ' + username + ' is connected')

        request('/addUser', {
            'chat_id': update.message.chat_id,
            'username': username
        })

        keyboard = [[
            InlineKeyboardButton(italian, callback_data='it'),
            InlineKeyboardButton(english, callback_data='en')
        ]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(unlock + 'Pantry unlocked! Please select your language', reply_markup=reply_markup)
        return LANG
    else:
        logging.info('User ' + str(update.message.chat_id) + ' put wrong password')
        update.message.reply_text(forbidden + 'Wrong password! Type /start to try again')
        return ConversationHandler.END


def lang_chooser(update, context):
    lang = update.callback_query
    request('/updateUserLang', {
        'lang': lang,
        'chat_id': context.chat_data['id']
    })
    lang.edit_message_text(_('LANGUAGE_SELECTED', update.message.chat_id))
    return ConversationHandler.END

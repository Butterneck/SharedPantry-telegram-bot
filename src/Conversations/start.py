from os import environ
from telegram.ext import ConversationHandler
from telegram import ReplyKeyboardMarkup
from emoji import emojize
import json

import logging

from src.Utils.BackendRequests import request

from src.Auth.authenticator import Authenticator

from src.Utils.Translator import translate as _, supported_langs

lock = emojize(":lock:", use_aliases=True)
unlock = emojize(":unlock:", use_aliases=True)
forbidden = emojize(":no_entry_sign:", use_aliases=True)
italian = emojize(':it:', use_aliases=True)
english = emojize(':uk:', use_aliases=True)


def start(update, context):
    from bot import AUTH
    if Authenticator().checkUserExistence(update.message.chat_id):
        if Authenticator().checkUserAdmin(update.message.chat_id):
            reply_markup = ReplyKeyboardMarkup([[_('PICK', update.message.chat_id), _('BILL', update.message.chat_id)], [_('DASHBOARD', update.message.chat_id)]])
        else:
            reply_markup = ReplyKeyboardMarkup([[_('PICK', update.message.chat_id)], [_('BILL', update.message.chat_id)]])
        update.message.reply_text(_('OLD_USER_WELCOME', update.message.chat_id), reply_markup=reply_markup)
        return ConversationHandler.END
    else:
        from src.Utils.Translator import load_translations
        logging.warning('New user ' + str(update.message.chat_id) + ' is connecting')
        update.message.reply_text(lock + ' ' + load_translations()['NEW_USER_WELCOME'][update._effective_user.language_code])
        return AUTH


def auth(update, context):
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

        lang = update._effective_user.language_code
        if not lang in supported_langs:
            lang = 'en'

        is_admin = True if json.loads(request('/getAllAdmins').text)['admins'] == [] else False
        request('/addUser', {
            'chat_id': update.message.chat_id,
            'username': username,
            'lang': lang,
            'is_admin': is_admin
        })
        if Authenticator().checkUserAdmin(update.message.chat_id):
            reply_markup = ReplyKeyboardMarkup([[_('PICK', update.message.chat_id), _('BILL', update.message.chat_id)],
                                                [_('DASHBOARD', update.message.chat_id)]])
        else:
            reply_markup = ReplyKeyboardMarkup(
                [[_('PICK', update.message.chat_id)], [_('BILL', update.message.chat_id)]])
        update.message.reply_text(unlock + _('PATRY_UNLOCKED', update.message.chat_id), reply_markup=reply_markup)
        return ConversationHandler.END
    else:
        from src.Utils.Translator import load_translations
        logging.info('User ' + str(update.message.chat_id) + ' put wrong password')
        update.message.reply_text(forbidden + load_translations()['WRONG_PANTRY_PASSWORD'][update._effective_user.language_code])
        return ConversationHandler.END

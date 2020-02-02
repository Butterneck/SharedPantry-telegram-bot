from os import environ
from src.Auth.authenticator import Authenticator
import logging

from src.Utils.Translator import translate as _


def dashboard(update):
    if not Authenticator().checkUserAdmin(update.message.chat_id):
        logging.warning('Non admin user asked for dashboard')
        return

    if environ['BACKEND_TOKEN'] is not None:
        update.message.reply_text(_('DASHBOARD', update.message.chat_id) + '/'.join([environ['FRONTEND_URL'], environ['BACKEND_TOKEN']]) + '\n' + _('REMEMBER_IS_TEMP', update.message.chat_id))
    else:
        update.message.reply_text(_('ERROR_ON_DASHBOARD', update.message.chat_id))

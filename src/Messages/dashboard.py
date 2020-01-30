from os import environ
from src.Auth.authenticator import Authenticator
import logging


def dashboard(bot, update):
    if not Authenticator().checkUserAdmin(update.message.chat_id):
        logging.warning('Non admin user asked for dashboard')
        return

    if environ['BACKEND_TOKEN'] is not None:
        update.message.reply_text("Here is dashboard link: " + '/'.join([environ['FRONTEND_URL'], environ['BACKEND_TOKEN']]))
    else:
        update.message.reply_text("Something went wrong on creating dashboard")
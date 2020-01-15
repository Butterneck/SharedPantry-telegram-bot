from os import environ, path
import logging
from configparser import ConfigParser

from ..Utils import TerminalColors
from src.DB.DBManager.db_connection_postgresql import DB_Connection

import telegram
from telegram.ext import Updater


class Configuration():

    def __init__(self, bot, updater):
        self.bot = bot
        self.updater = updater

    def determine_env(self):
        if "TOKEN" in environ:
            logging.info("Running in production mode")
            return "Production"
        else:
            logging.info("Running in local test mode")
            return "LocalTest"

    def configure_env(self, env, updater, db_manager):
        if env == "Production":
            self.configure_production(updater, db_manager)
        elif env == "LocalTest":
            self.configure_local_test(updater, db_manager)
        updater.idle()

    def configure_production(self, updater, db_manager):
        db_url = environ['DATABASE_URL']
        sslRequired = True
        db_name = "Production_DB"
        db_manager = DB_Connection(db_url, sslRequired, db_name)
        logging.info(TerminalColors.WARNING + 'Starting Webhook' + TerminalColors.ENDC)
        updater.start_webhook(listen='0.0.0.0',
                              port=int(environ.get('PORT', '8443')),
                              url_path=environ['TOKEN'])
        updater.bot.set_webhook("https://" + environ['APPNAME'] + ".herokuapp.com/" + environ['TOKEN'])

    def configure_local_test(self, updater, db_manager):
        if not path.isfile('../../.config/Bot/config.ini'):
            self.first_local_config()
        config = ConfigParser.read_file(open('../../.config/Bot/config.ini'))
        db_url = "postgres://" + config['DB']['username'] + (":" + config['DB']['password'] if config['DB']['password'] != '' else '') + "@localhost/" + config['DB']['name']
        sslRequired = False
        db_name = "LocalTest_DB"
        db_manager = DB_Connection(db_url, sslRequired, db_name)
        logging.info(TerminalColors.WARNING + 'Starting Polling' + TerminalColors.ENDC)
        updater.start_polling()

    def first_local_config(self):
        # Ask for parameters to be saved in local config and save them to .config/Bot/config.ini

    def configure(self, bot, updater):
        updater = Updater(environ['TOKEN'])
        bot = telegram.Bot(environ['TOKEN'])
        db_manager = DB_Connection()
        self.configure_env(self.determine_env(), updater, db_manager)

from os import environ, path
import logging
from configparser import ConfigParser

from ..Utils import TerminalColors
from src.DB.DBManager.db_connection_postgresql import DB_Connection

import telegram
from telegram.ext import Updater


class Configuration():
    def determine_env(self):
        if "TOKEN" in environ:
            logging.info("Running in production mode")
            return "Production"
        else:
            logging.info("Running in local test mode")
            return "LocalTest"

    def configure_production(self, updater, bot):
        db_url = environ['DATABASE_URL']
        sslRequired = True
        db_name = "Production_DB"
        db_manager = DB_Connection(db_url, sslRequired, db_name)
        logging.info(TerminalColors.WARNING + 'Starting Webhook' + TerminalColors.ENDC)
        updater.start_webhook(listen='0.0.0.0',
                              port=int(environ.get('PORT', '8443')),
                              url_path=environ['TOKEN'])
        updater.bot.set_webhook("https://" + environ['APPNAME'] + ".herokuapp.com/" + environ['TOKEN'])
        return [updater, bot, db_manager]

    def configure_local_test(self):
        if not path.isfile('../../.config/Bot/config.ini'):
            self.first_local_config()
        config = ConfigParser.read_file(open('../../.config/Bot/config.ini'))
        db_url = "postgres://" + config['DB']['username'] + (":" + config['DB']['password'] if config['DB']['password'] != '' else '') + "@" + config['DB']['host'] + "/" + config['DB']['name']
        sslRequired = False
        db_name = "LocalTest_DB"
        db_manager = DB_Connection(db_url, sslRequired, db_name)
        updater = Updater(config['BOT']['TOKEN'])
        bot = telegram.Bot(config['BOT']['TOKEN'])
        logging.info(TerminalColors.WARNING + 'Starting Polling' + TerminalColors.ENDC)
        updater.start_polling()
        return [updater, bot, db_manager]

    def first_local_config(self):
        # Ask for parameters to be saved in local config and save them to .config/Bot/config.ini
        print('This is the first time you run this bot in LocalTest mode, let\'s config the environment:\n')
        config = ConfigParser()
        config['BOT']['TOKEN'] = input('Bot TOKEN: ')
        config['DB']['username'] = input('Database username: ')
        config['DB']['password'] = input('Database password: ')
        config['DB']['host'] = input('Database host: ')
        config['DB']['name'] = input('Database name: ')
        print('Cool! You have configured the environment!')
        with open('../../.config/Bot/config.ini', 'w') as configfile:
            config.write(configfile)

    def configure(self):
        env = self.determine_env()
        updater = None
        bot = None,
        db_manager = None
        if env == "Production":
            updater = Updater(environ['TOKEN'])
            bot = telegram.Bot(environ['TOKEN'])
            updater, bot, db_manager = self.configure_production(updater, bot)
        elif env == "LocalTest":
            updater, bot, db_manager = self.configure_local_test()
        if updater and bot and db_manager is not None:
            updater.idle()
            return [updater, bot, db_manager]
        else:
            logging.error('Something went wrong on configuration')

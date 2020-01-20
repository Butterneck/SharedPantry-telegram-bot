from os import environ, path
import logging
from configparser import ConfigParser

from ..Utils import TerminalColors

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

    def configure_local_test(self):
        config = ConfigParser()
        if not path.isfile('.config/Bot/config.ini'):
            self.first_local_config(config)
        config.read_file(open('.config/Bot/config.ini'))
        updater = Updater(config['BOT']['TOKEN'])
        bot = telegram.Bot(config['BOT']['TOKEN'])
        return [updater, bot]

    def first_local_config(self, config):
        # Ask for parameters to be saved in local config and save them to .config/Bot/config.ini
        print('This is the first time you run this bot in LocalTest mode, let\'s config the environment:\n')
        config['BOT'] = {}
        config['BOT']['TOKEN'] = input('Bot TOKEN: ')
        print('Cool! You have configured the environment!')
        with open('.config/Bot/config.ini', 'w') as configfile:
            config.write(configfile)

    def configure(self):
        env = self.determine_env()
        updater = None
        bot = None,
        db_manager = None
        if env == "Production":
            updater = Updater(environ['TOKEN'])
            bot = telegram.Bot(environ['TOKEN'])

        elif env == "LocalTest":
            updater, bot = self.configure_local_test()
        if updater and bot and db_manager is not None:
            return [updater, bot]
        else:
            logging.error('Something went wrong on configuration')

    def start_listening(self, updater):
        if self.determine_env() == 'Production':
            logging.info(TerminalColors.WARNING + 'Starting Webhook' + TerminalColors.ENDC)
            updater.start_webhook(listen='0.0.0.0',
                                  port=int(environ.get('PORT', '8443')),
                                  url_path=environ['TOKEN'])
            updater.bot.set_webhook("https://" + environ['APPNAME'] + ".herokuapp.com/" + environ['TOKEN'])
        elif self.determine_env() == 'LocalTest':
            print(TerminalColors.WARNING + 'Starting Polling' + TerminalColors.ENDC)
            updater.start_polling()
        else:
            logging.error('Something went wrong on configuration')
            return
        updater.idle()
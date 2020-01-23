from os import environ, path
import logging
from configparser import ConfigParser

import requests

import telegram
from telegram.ext import Updater

import json


class Configuration():
    def determine_env(self):
        if "BOT_TOKEN" in environ:
            logging.info("Running in production mode")
            environ['env'] = 'Production'
            return "Production"
        else:
            logging.info("Running in local test mode")
            environ['env'] = 'LocalTest'
            return "LocalTest"

    def configure_local_test(self):
        config = ConfigParser()
        if not path.isfile('.config/Bot/config.ini'):
            logging.warning('Running FirstTime local config')
            self.first_local_config(config)
        config.read_file(open('.config/Bot/config.ini'))
        environ['BOT_TOKEN'] = config['BOT']['TOKEN']
        r = requests.post('/getToken', json={'token': environ['BOT_TOKEN']})
        if r.status_code == 200:
            environ['BACKEND_TOKEN'] = json.loads(r.text)['token']
        elif r.status_code == 500:
            logging.error('/getToken returned 500, stopping')
            exit(1)
        elif r.status_code == 403:
            logging.error('/getToken got wrong bot token')
            exit(1)
        updater = Updater(environ['BOT_TOKEN'])
        bot = telegram.Bot(environ['BOT_TOKEN'])
        return updater, bot

    def first_local_config(self, config):
        # Ask for parameters to be saved in local config and save them to .config/Bot/config.ini
        print('This is the first time you run this bot in LocalTest mode, let\'s config the environment:\n')
        config['BOT'] = {}
        config['BOT']['TOKEN'] = input('Bot TOKEN: ')
        with open('.config/Bot/config.ini', 'w') as configfile:
            config.write(configfile)
        print('Cool! You have configured the environment!\nConfiguration file can be found on .config/Bot/config.ini')
        logging.info('Configuration correctly saved on .config/Bot/config.ini')

    def configure(self):
        # Getting backend token
        env = self.determine_env()
        updater = None
        bot = None
        if env == "Production":
            logging.warning('Running in ProductionMode')
            r = requests.post('/getToken', json={'token': environ['BOT_TOKEN']})
            if r.status_code == 200:
                environ['BACKEND_TOKEN'] = json.loads(r.text)['token']
            elif r.status_code == 500:
                logging.error('/getToken returned 500, stopping')
                exit(1)
            elif r.status_code == 403:
                logging.error('/getToken got wrong bot token')
                exit(1)
            updater = Updater(environ['BOT_TOKEN'])
            bot = telegram.Bot(environ['BOT_TOKEN'])
        elif env == "LocalTest":
            logging.warning('Running in LocalTestMode')
            updater, bot = self.configure_local_test()
        if updater and bot is not None:
            return updater, bot
        else:
            logging.error('Something went wrong on configuration')
            exit(1)

    def start_listening(self, updater):
        if environ['env'] == 'Production':
            logging.warning('Starting Webhook')
            updater.start_webhook(listen='0.0.0.0',
                                  port=int(environ.get('PORT', '8443')),
                                  url_path=environ['BOT_TOKEN'])
            updater.bot.set_webhook("https://" + environ['APPNAME'] + ".herokuapp.com/" + environ['BOT_TOKEN'])
        elif environ['env'] == 'LocalTest':
            logging.warning('Starting Polling')
            updater.start_polling()
        else:
            logging.error('Something went wrong on configuration')
            exit(1)
        updater.idle()
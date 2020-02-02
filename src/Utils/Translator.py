import yaml
from src.Utils.BackendRequests import request
import json
import logging


supported_langs = ['en', 'it']


def load_translations():
    t = yaml.load(open('i18n/translations.yml'), Loader=yaml.CLoader)
    return t


def translate(string, chat_id):
    r = request('/getUserFromChatId', {
        'chat_id': chat_id
    })
    print(r)
    if r.status_code == 200:
        return load_translations()[string][json.loads(r.text)['user']['lang']]
    elif r.status_code == 500:
        logging.info('User ' + str(chat_id) + ' is not logged in')
        return False
    elif r.status_code == 403:
        logging.warning('Wrong backend token')
        exit(1)

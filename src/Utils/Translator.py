import yaml
from src.Utils.BackendRequests import request


def load_translations():
    t = yaml.load(open('i18n/translations.yml'), Loader=yaml.CLoader)
    return t


def translate(string, chat_id):
    lang = request('/getUserFromChatId', {
        'chat_id': chat_id
    })['user']['lang']
    t = load_translations()
    return t[string][lang]

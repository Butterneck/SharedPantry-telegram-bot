import json
import logging

from src.Utils.BackendRequests import request


class Authenticator():
    def checkUserExistence(self, chat_id):
        logging.info('Checking user ' + str(chat_id) + ' existence')
        r = request('/getUserFromChatId', {'chat_id': chat_id})
        if r.status_code == 200:
            return json.loads(r.text)['user'] is not None
        elif r.status_code == 500:
            logging.info('User ' + chat_id + ' is not logged in')
            return False
        elif r.status_code == 403:
            logging.warning('Wrong backend token')
            exit(1)

    def checkUserAdmin(self, chat_id):
        r = request('/getUserFromChatId', {'chat_id': chat_id})
        if r.status_code == 200:
            if json.loads(r.text)['is_admin']:
                logging.info('User ' + json.loads(r.text)['username'] + ' is an admin')
                return True
            else:
                logging.info('User ' + json.loads(r.text)['username'] + ' is not an admin')
                return False
        elif r.status_code == 500:
            logging.info('User ' + str(chat_id) + ' is not logged in')
            return False
        elif r.status_code == 403:
            logging.warning('Wrong backend token')
            exit(1)

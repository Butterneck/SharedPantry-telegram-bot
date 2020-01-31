from requests import post
from os import environ

import logging


def request(path, data=None):
    logging.info('requesting ' + path)
    logging.info('token:' + environ['BACKEND_TOKEN'])
    r = post(environ['BACKEND_URL'] + '/api' + path, json=data, headers={'token': environ['BACKEND_TOKEN']})
    return r


def validate_response(r):
    if r.status_code == 200:
        return True
    elif r.status_code == 500:
        logging.error('request returned 500, stopping')
        return False
    elif r.status_code == 400:
        logging.error('request is malformed')
        return False
    elif r.status_code == 403:
        logging.error('backend got wrong bot token')
        return False

from requests import post
from os import environ

import logging


def request(path, data = {}):
    json = {
        'token': environ['BACKEND_TOKEN'],
        'data': data
    }
    logging.info('requesting ' + path)
    return post(environ['BACKEND_URL'] + path, json=json)


def validate_response(r):
    if r.status_code == 200:
        return True
    elif r.status_code == 500:
        logging.error('request returned 500, stopping')
        return False
    elif r.status_code == 403:
        logging.error('backend got wrong bot token')
        return False

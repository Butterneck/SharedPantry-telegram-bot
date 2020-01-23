from requests import post
from os import environ


def request(path, data):
    json = {
        'token': environ['BACKEND_TOKEN'],
        'data': data
    }
    return post(environ['BACKEND_URL'] + path, json=json)
from os import environ
import json
import requests


def dashboard(bot, update):
    environ['BACKEND_TOKEN'] = json.loads(requests.post(
        environ['BACKEND_URL'] + '/getToken',
        json = {
            'token': environ['BOT_TOKEN']
        }
    ))

    if environ['BACKEND_TOKEN'] is not None:
        update.message.reply_text("Here is dashboard link: " + '/?token='.join([environ['BACKEND_URL'], environ['BACKEND_TOKEN']]))
    else:
        update.message.reply_text("Something went wrong on creating dashboard")
import telegram
import logging
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

# Funzioni ausiliarie
from gestisci_ordine import start, button


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    TOKEN = "757571867:AAHrPE1iyZ5FrWoH412U9Ubq6sO-tFA29jM"
    updater = Updater(TOKEN)
    bot = telegram.Bot(TOKEN)


    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

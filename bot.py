import telegram
from telegram.ext import Updater

# Funzioni ausiliarie



def main():
    TOKEN = "757571867:AAHrPE1iyZ5FrWoH412U9Ubq6sO-tFA29jM"
    updater = Updater(TOKEN)
    bot = telegram.Bot(TOKEN)


    dp = updater.dispatcher

    dp.add_handler(CommandHandler("prendi", prendi))
    dp.add_handler(CommandHandler("lista", lista))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

from src.Configuration.Configure import Configuration
import logging
from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, Filters, CallbackQueryHandler
from src.Messages.help import help
from src.Messages.dashboard import dashboard
from src.Messages.pick import pick, button
from src.Messages.bill import send_bill_message, send_monthly_bill_message

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

AUTH, LANG = range(2)

from src.Conversations.start import start, auth, lang_chooser


def main():
    updater, bot = Configuration().configure()

    conv_handler_start = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            AUTH: [MessageHandler(Filters.text, auth)],
            LANG: [CallbackQueryHandler(lang_chooser)]
        },
        fallbacks=[]
    )

    dp = updater.dispatcher
    dp.add_handler(conv_handler_start)
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(CommandHandler('dashboard', dashboard))
    dp.add_handler(CommandHandler('pick', pick))
    dp.add_handler(CommandHandler('prendi', pick))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(CommandHandler('bill', send_bill_message))
    dp.add_handler(CommandHandler('conto', send_bill_message))
    dp.add_handler(CommandHandler('month', send_monthly_bill_message))
    dp.add_handler(CommandHandler('contomensile', send_monthly_bill_message))

    Configuration().start_listening(updater)


if __name__ == '__main__':
    main()

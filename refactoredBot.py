from src.Configuration.Configure import Configuration
import logging
from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, Filters, CallbackQueryHandler
from src.Messages import help
from src.Messages import dashboard
from src.Messages.pick import pick, button

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

AUTH = range(1)

from src.Conversations.start import start, auth


def main():
    updater, bot = Configuration().configure()

    conv_handler_start = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            AUTH: [MessageHandler(Filters.text, auth)]
        },
        fallbacks=[]
    )

    dp = updater.dispatcher
    dp.add_handler(conv_handler_start)
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(CommandHandler('dashboard', dashboard))
    dp.add_handler(CommandHandler('pick', pick))
    dp.add_handler(CallbackQueryHandler(button))

    Configuration().start_listening(updater)


if __name__ == '__main__':
    main()

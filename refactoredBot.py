from src.Configuration.Configure import Configuration
import logging
from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, Filters
from src.Messages import help
from src.Conversations.start import start, auth

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

AUTH = range(1)


def main():
    updater, bot = Configuration().configure()

    conv_handler_start = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            AUTH: [MessageHandler(Filters.text, auth)]
        }
    )

    dp = updater.dispatcher
    dp.add_handler(conv_handler_start)
    dp.add_handler(CommandHandler('help', help))


if __name__ == '__main__':
    main()
from src.Utils.Translator import translate as _


def help(update, context):
    help_message = (_('HELP', update.message.chat_id))
    update.message.reply_text(help_message)

import logging

from environs import Env
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger('Logger')


def start(update, context):
    update.message.reply_text('Привет!')


def echo(update, context):
    update.message.reply_text(update.message.text)


if __name__ == '__main__':
    env = Env()
    env.read_env()

    updater = Updater(env.str('TELEGRAM_BOT_TOKEN'))
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()
    updater.idle()

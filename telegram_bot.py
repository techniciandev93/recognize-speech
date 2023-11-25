import json
import logging
from functools import partial

from environs import Env
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from intent import detect_intent_texts

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger('Logger')


def start(update, context):
    update.message.reply_text('Привет!')


def run_dialog_flow_telegram(update, context, project_id, language_code):
    message = detect_intent_texts(project_id, update.message.from_user.id, update.message.text, language_code)
    if message:
        update.message.reply_text(message)


if __name__ == '__main__':
    env = Env()
    env.read_env()

    language_code = 'ru_RU'
    google_application_credentials_path = env.str('GOOGLE_APPLICATION_CREDENTIALS')

    with open(google_application_credentials_path, 'r', encoding='utf8') as file:
        credentials = json.load(file)

    updater = Updater(env.str('TELEGRAM_BOT_TOKEN'))
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))

    dialog_flow_with_args = partial(run_dialog_flow_telegram,
                                    project_id=credentials['quota_project_id'],
                                    language_code=language_code)
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, dialog_flow_with_args))

    updater.start_polling()
    updater.idle()

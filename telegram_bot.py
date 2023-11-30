import json
import logging
from functools import partial

import telegram
from environs import Env
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from intent import detect_intent_texts
from telegram_logging_handler import TelegramLogsHandler


logger = logging.getLogger('Logger telegram bot')


def start(update, context):
    update.message.reply_text('Привет!')


def send_dialog_flow_tg(update, context, project_id, language_code):
    dialogflow_response = detect_intent_texts(project_id, update.message.from_user.id, update.message.text, language_code)
    update.message.reply_text(dialogflow_response.fulfillment_text)


if __name__ == '__main__':
    try:
        env = Env()
        env.read_env()

        telegram_chat_id = env.str('TELEGRAM_CHAT_ID')
        telegram_bot_token = env.str('TELEGRAM_BOT_TOKEN')
        telegram_notification_token = env.str('TELEGRAM_NOTIFICATION_TOKEN')
        google_application_credentials_path = env.str('GOOGLE_APPLICATION_CREDENTIALS')

        updater = Updater(telegram_bot_token)
        notification_bot = telegram.Bot(token=telegram_notification_token)

        language_code = 'ru_RU'

        with open(google_application_credentials_path, 'r', encoding='utf8') as file:
            credentials = json.load(file)

        dispatcher = updater.dispatcher
        dispatcher.add_handler(CommandHandler('start', start))

        dialog_flow_with_args = partial(send_dialog_flow_tg,
                                        project_id=credentials['quota_project_id'],
                                        language_code=language_code)
        dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, dialog_flow_with_args))

        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
        )

        logger.setLevel(logging.INFO)
        logger.addHandler(TelegramLogsHandler(notification_bot, telegram_chat_id))

        logger.info('Бот телеграмм запущен')
        updater.start_polling()
        updater.idle()
    except Exception as error:
        logger.exception(error)

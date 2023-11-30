import json
import logging
import random

import telegram
import vk_api
from environs import Env
from vk_api.longpoll import VkLongPoll, VkEventType

from intent import detect_intent_texts
from telegram_logging_handler import TelegramLogsHandler


logger = logging.getLogger('Logger vk bot')


def send_dialog_flow_vk(event, vk_api, project_id, language_code):
    dialogflow_response = detect_intent_texts(project_id, event.user_id, event.text, language_code)
    if not dialogflow_response.intent.is_fallback:
        vk_api.messages.send(
            user_id=event.user_id,
            message=dialogflow_response.fulfillment_text,
            random_id=random.randint(1, 1000)
        )


if __name__ == '__main__':
    try:
        env = Env()
        env.read_env()
        vk_token = env.str('VK_GROUP_TOKEN')
        google_application_credentials_path = env.str('GOOGLE_APPLICATION_CREDENTIALS')
        telegram_notification_token = env.str('TELEGRAM_NOTIFICATION_TOKEN')
        telegram_chat_id = env.str('TELEGRAM_CHAT_ID')

        language_code = 'ru_RU'

        with open(google_application_credentials_path, 'r', encoding='utf8') as file:
            credentials = json.load(file)

        vk_session = vk_api.VkApi(token=vk_token)
        vk_api = vk_session.get_api()
        longpoll = VkLongPoll(vk_session)

        notification_bot = telegram.Bot(token=telegram_notification_token)

        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
        )

        logger.setLevel(logging.INFO)
        logger.addHandler(TelegramLogsHandler(notification_bot, telegram_chat_id))
        logger.info('Бот вконтакте запущен')

        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                send_dialog_flow_vk(event, vk_api, credentials['quota_project_id'], language_code)

    except Exception as error:
        logger.exception(error)

import json
import random

import vk_api
from environs import Env
from vk_api.longpoll import VkLongPoll, VkEventType

from intent import detect_intent_texts


def run_dialog_flow_vk(event, vk_api, project_id, language_code):
    message = detect_intent_texts(project_id, event.user_id, event.text, language_code)
    if message:
        vk_api.messages.send(
            user_id=event.user_id,
            message=message,
            random_id=random.randint(1, 1000)
        )


if __name__ == '__main__':
    env = Env()
    env.read_env()
    vk_bot_token = env.str('VK_BOT_TOKEN')
    google_application_credentials_path = env.str('GOOGLE_APPLICATION_CREDENTIALS')

    language_code = 'ru_RU'

    with open(google_application_credentials_path, 'r', encoding='utf8') as file:
        credentials = json.load(file)

    vk_session = vk_api.VkApi(token=vk_bot_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            run_dialog_flow_vk(event, vk_api, credentials['quota_project_id'], language_code)

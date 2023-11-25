import vk_api
from environs import Env
from vk_api.longpoll import VkLongPoll, VkEventType


def run_longpoll_vk(longpoll):
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            print('Новое сообщение:')
            if event.to_me:
                print('Для меня от: ', event.user_id)
            else:
                print('От меня для: ', event.user_id)
            print('Текст:', event.text)


if __name__ == '__main__':
    env = Env()
    env.read_env()
    vk_bot_token = env.str('VK_BOT_TOKEN')

    vk_session = vk_api.VkApi(token=vk_bot_token)

    longpoll_vk = VkLongPoll(vk_session)
    run_longpoll_vk(longpoll_vk)

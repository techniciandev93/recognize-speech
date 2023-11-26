# Распознаем сообщения c помощью DialogFlow

Боты для Телеграм и Вконтакте которые умеет отвечать на типичные вопросы при помощи [DialogFlow](https://cloud.google.com/dialogflow/docs)


## Как установить

Python 3.8 должен быть уже установлен.
Затем используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```

Создайте файл `.env` в корневой директории проекта и добавьте переменные окружения:

```
TELEGRAM_BOT_TOKEN= токен телеграмм бота
GOOGLE_APPLICATION_CREDENTIALS= путь до файла credentials.json с ключами для подключения к Google API.
VK_GROUP_TOKEN= ключ доступа к группе VK.
TELEGRAM_NOTIFICATION_TOKEN= токен для 2 бота уведомлений
TELEGRAM_CHAT_ID= ваш ID в телеграмме
```
## Как запустить
Для запуска телеграм бота
```
python telegram_bot.py
```
Для запуска бота vk
```
python vk_bot.py
```
Запустите скрипт, чтобы обучить агента
```
python intent.py
```
Для обучения используется файл questions.json в корне проекта

## Примечания

- Для работы скрипта необходимо иметь 2 API-токена Telegram (1 бот для отправки уведомлений о проверенных работах, 2 бот для отправки уведомлений о работе 1 бота). Вы можете получить их, создав ботов через [BotFather](https://core.telegram.org/bots#botfather).
- Для корректной работы скрипта, убедитесь, что у вас есть `chat_id`, который представляет уникальный идентификатор чата в Telegram. Можно узнать сво ID  у бота [userinfobot](https://t.me/userinfobot).
- В группе ВК, в меню справа находим пункт Управление, затем Работа с API, и создаем ключ доступа. Далее Сообщения ⟶ Настройки для бота и включаем "Возможности ботов".

Для работы с Dialogflow понадобится:
- Создайте проект в [Google Cloud](https://cloud.google.com/dialogflow/es/docs/quick/setup#project)
- Создайте ["агента"](https://cloud.google.com/dialogflow/es/docs/quick/build-agent), который будет отвечать на вопросы.
- Зарегистрируйте сервисный аккаунт для проекта. Чтобы получить файл с ключами от вашего Google-аккаунта, credentials.json используйте [gcloud](https://cloud.google.com/dialogflow/es/docs/quick/setup#sdk).

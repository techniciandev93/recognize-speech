import json
import logging
from functools import partial

from environs import Env
from google.cloud import dialogflow
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger('Logger')


def detect_intent_texts(project_id, user_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, user_id)
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    return response.query_result.fulfillment_text


def start(update, context):
    update.message.reply_text('Привет!')


def echo(update, context, project_id, language_code):
    message = detect_intent_texts(project_id, update.message.from_user.id, update.message.text, language_code)
    update.message.reply_text(message)


if __name__ == '__main__':
    env = Env()
    env.read_env()

    language_code = 'ru_RU'
    google_application_credentials_path = env.str('GOOGLE_APPLICATION_CREDENTIALS')

    with open(google_application_credentials_path, 'r') as file:
        credentials = json.load(file)

    updater = Updater(env.str('TELEGRAM_BOT_TOKEN'))
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))

    echo_with_args = partial(echo, project_id=credentials['quota_project_id'], language_code=language_code)
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo_with_args))

    updater.start_polling()
    updater.idle()

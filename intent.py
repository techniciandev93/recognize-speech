import argparse
import json
import logging

from environs import Env
from google.cloud import dialogflow


logger = logging.getLogger('Logger intent')


def create_intent(project_id, display_name, training_phrases_parts, answer_text):
    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=[answer_text])
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    intents_client.create_intent(
        request={'parent': parent, 'intent': intent}
    )


def detect_intent_texts(project_id, user_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, user_id)
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={'session': session, 'query_input': query_input}
    )
    return response.query_result


if __name__ == '__main__':
    try:
        env = Env()
        env.read_env()

        parser = argparse.ArgumentParser(description="Этот скрипт предназначен для обучения агента "
                                                     "по умолчанию без аргументов будет браться файл questions.json "
                                                     "из корня проекта: python intent.py")
        parser.add_argument('--path', type=str, help="Укажите путь к json файлу",
                            nargs='?', default='questions.json')
        args = parser.parse_args()

        google_application_credentials_path = env.str('GOOGLE_APPLICATION_CREDENTIALS')

        with open(google_application_credentials_path, 'r', encoding='utf8') as file:
            credentials = json.load(file)

        with open(args.path, 'r', encoding='utf8') as file:
            questions = json.load(file)

        for intent_name, intent in questions.items():
            create_intent(
                credentials['quota_project_id'],
                intent_name,
                intent['questions'],
                intent['answer']
            )

        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
        )

        logger.setLevel(logging.ERROR)
    except Exception as error:
        logger.exception(error)

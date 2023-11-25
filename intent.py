import json

from environs import Env
from google.cloud import dialogflow


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

    response = intents_client.create_intent(
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
    return response.query_result.fulfillment_text


if __name__ == '__main__':
    env = Env()
    env.read_env()

    questions_path = 'questions.json'

    google_application_credentials_path = env.str('GOOGLE_APPLICATION_CREDENTIALS')

    with open(google_application_credentials_path, 'r', encoding='utf8') as file:
        credentials = json.load(file)

    with open(questions_path, 'r', encoding='utf8') as file:
        questions = json.load(file)

    for intent_name in questions:
        create_intent(
            credentials['quota_project_id'],
            intent_name,
            questions[intent_name]['questions'],
            questions[intent_name]['answer']
        )

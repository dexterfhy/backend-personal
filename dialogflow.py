from google.cloud import dialogflow
from google.oauth2 import service_account

from beans.session import Session
from constants import GOOGLE_SERVICE_ACCOUNT_FILE_PATH, DEFAULT_DIALOGFLOW_LANGUAGE_CODE, DIALOGFLOW_PROJECT_ID, \
    CUSTOM_EVENTS
from intent_handlers import INTENT_HANDLERS, __display_default_response
from utils import default_if_blank

credentials = service_account.Credentials.from_service_account_file(GOOGLE_SERVICE_ACCOUNT_FILE_PATH)
session_client = dialogflow.SessionsClient(credentials=credentials)


# Calls Dialogflow API to trigger an intent match
# Calls the corresponding function handler for the intent result action if present
def process_user_input(session: Session, user_input, cache):
    intent_result = detect_intent_via_event(session.chat_session_id, user_input) if user_input in CUSTOM_EVENTS \
        else detect_intent_via_text(session.chat_session_id, user_input)

    intent_action = default_if_blank(intent_result.action, 'DISPLAY_DEFAULT_RESPONSE')

    return INTENT_HANDLERS.get(intent_action, __display_default_response)(session, user_input, intent_result, cache)


# Attempts to match an intent with given free text input
def detect_intent_via_text(session_id, text):
    text_input = dialogflow.TextInput(text=text, language_code=DEFAULT_DIALOGFLOW_LANGUAGE_CODE)

    return __detect_intent(session_id, dialogflow.QueryInput(text=text_input))


# Attempts to match an intent with given event input
def detect_intent_via_event(session_id, event):
    event_input = dialogflow.EventInput(name=event, language_code=DEFAULT_DIALOGFLOW_LANGUAGE_CODE)

    return __detect_intent(session_id, dialogflow.QueryInput(event=event_input))


def __detect_intent(session_id, query_input):
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, session_id)

    response = session_client.detect_intent(request={'session': session, 'query_input': query_input})

    return response.query_result

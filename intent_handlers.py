
from datetime import datetime

from beans.session import Session
from cache import set_feedback, get_feedback
from constants import DEFAULT_ERROR_MESSAGE, DEFAULT_FALLBACK_MESSAGE, GET_CHATBOT_RESPONSES, GET_CHATBOT_OPTIONS, \
    FEEDBACK_TEMPLATE, BOT_USER_TYPE
from telegram import send_message
from utils import default_if_blank, get_random_prompts


# Returns a generic fallback message
def handle_invalid_intent(session: Session, user_input, intent_result, cache):
    return __build_response(DEFAULT_FALLBACK_MESSAGE, {})


# Displays the response found in the intent result as is, with no options
def __display_default_response(session: Session, user_input, intent_result, cache):
    response = default_if_blank(intent_result.fulfillment_text, DEFAULT_ERROR_MESSAGE)
    return __build_response(response, {})


def __display_default_response_without_prompts(session: Session, user_input, intent_result, cache):
    response = default_if_blank(intent_result.fulfillment_text, DEFAULT_ERROR_MESSAGE)
    return __build_response(response, {}, False)


def __greet_name(session: Session, user_input, intent_result, cache):
    response = GET_CHATBOT_RESPONSES['GREETING_WITH_NAME'](intent_result.output_contexts[0].parameters['person']['name'])
    return __build_response(response, {})


def __display_contact_details(session: Session, user_input, intent_result, cache):
    response = GET_CHATBOT_RESPONSES['CONTACT_DETAILS']()
    return __build_response(response, GET_CHATBOT_OPTIONS['WHATSAPP'])


def __display_education_timeline(session: Session, user_input, intent_result, cache):
    response = GET_CHATBOT_RESPONSES['EDUCATION']()
    return __build_response(response, GET_CHATBOT_OPTIONS['EDUCATION'])


def __display_employment_timeline(session: Session, user_input, intent_result, cache):
    response = GET_CHATBOT_RESPONSES['EMPLOYMENT']()
    return __build_response(response, GET_CHATBOT_OPTIONS['EMPLOYMENT'])


def __show_chatbot_articles(session: Session, user_input, intent_result, cache):
    response = GET_CHATBOT_RESPONSES['CHATBOT']()
    return __build_response(response, GET_CHATBOT_OPTIONS['CHATBOT'])


def __show_kitties(session: Session, user_input, intent_result, cache):
    response = GET_CHATBOT_RESPONSES['KITTIES']()
    return __build_response(response, GET_CHATBOT_OPTIONS['KITTIES'])


def __show_cancel(session: Session, user_input, intent_result, cache):
    response = default_if_blank(intent_result.fulfillment_text, DEFAULT_ERROR_MESSAGE)
    return __build_response(response, GET_CHATBOT_OPTIONS['CANCEL'], False)


def __confirm_feedback(session: Session, user_input, intent_result, cache):
    response = GET_CHATBOT_RESPONSES['CONFIRM_FEEDBACK'](user_input)
    set_feedback(session.chat_session_id, user_input, cache)
    return __build_response(response, GET_CHATBOT_OPTIONS['CONFIRM_FEEDBACK'], False)


def __confirm_feedback_fallback(session: Session, user_input, intent_result, cache):
    response = default_if_blank(intent_result.fulfillment_text, DEFAULT_ERROR_MESSAGE)
    return __build_response(response, GET_CHATBOT_OPTIONS['CONFIRM_FEEDBACK'], False)


def __submit_feedback(session: Session, user_input, intent_result, cache):
    response = default_if_blank(intent_result.fulfillment_text, DEFAULT_ERROR_MESSAGE)
    feedback = FEEDBACK_TEMPLATE \
        .format(session.socket_session_id,
                default_if_blank(intent_result.output_contexts[0].parameters['email'],
                                 default_if_blank(intent_result.output_contexts[0].parameters['number'], 'N.A.')),
                get_feedback(session.chat_session_id, cache))
    send_message(feedback)
    return __build_response(response, {}, True)


def __build_response(text, options, show_random_prompts=True):
    return {
        "type": BOT_USER_TYPE,
        "text": text,
        "date": datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
        "options": options,
        "prompts": get_random_prompts() if show_random_prompts else []
    }


# Dictionary of intent actions mapped to a corresponding function that will be executed when the intent is matched
INTENT_HANDLERS = {
    'DISPLAY_DEFAULT_RESPONSE': __display_default_response,
    'DISPLAY_DEFAULT_RESPONSE_WITHOUT_PROMPTS': __display_default_response_without_prompts,
    'GREET_NAME': __greet_name,
    'DISPLAY_CONTACT_DETAILS': __display_contact_details,
    'DISPLAY_EDUCATION_TIMELINE': __display_education_timeline,
    'DISPLAY_EMPLOYMENT_TIMELINE': __display_employment_timeline,
    'SHOW_CHATBOT_ARTICLES': __show_chatbot_articles,
    'SHOW_KITTIES': __show_kitties,
    'SHOW_CANCEL': __show_cancel,
    'CONFIRM_FEEDBACK': __confirm_feedback,
    'CONFIRM_FEEDBACK_FALLBACK': __confirm_feedback_fallback,
    'SUBMIT_FEEDBACK': __submit_feedback,
}

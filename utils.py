# Returns given string if it is not None or blank, else return default value provided
import random

from constants import RANDOM_PROMPTS_SIZE, PROMPTS


def default_if_blank(s, default):
    if is_not_blank(s):
        return s
    else:
        return default


def is_not_blank(*string):
    return all(s is not None and s for s in string)


def get_random_prompts():
    prompts = []
    while len(prompts) < RANDOM_PROMPTS_SIZE:
        new_prompt = random.choice(PROMPTS)
        if new_prompt not in prompts:
            prompts.append(new_prompt)

    return list(map(__to_option, prompts))


# Extracts user id from Telegram request
def get_user_id_from_request(req_body):
    if 'callback_query' in req_body:
        return req_body.get('callback_query', {}).get('from', {}).get('id', '')
    elif 'message' in req_body:
        return req_body.get('message', {}).get('from', {}).get('id', '')
    else:
        return ''


# Extracts user's input (text or button click) from Telegram request
def get_user_input_from_request(req_body):
    if 'callback_query' in req_body:
        return req_body.get('callback_query', {}).get('data', '')
    elif 'message' in req_body:
        return req_body.get('message', {}).get('text', '')
    else:
        return ''


def __to_option(prompt_text):
    return {
        "text": prompt_text
    }

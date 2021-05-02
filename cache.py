import uuid

from beans.session import Session
from utils import default_if_blank, is_not_blank


# Returns a session id for the current user, or generates a new one (UUID)
def get_current_session(user_session_id, cache):
    session_key = __session_key(user_session_id)
    session_id = cache.get(session_key)

    if is_not_blank(session_id):
        return Session(user_session_id, session_id, False)
    else:
        new_session_id = uuid.uuid4().hex
        cache.set(session_key, new_session_id)
        return Session(user_session_id, new_session_id, True)


def clear_current_session(user_session_id, cache):
    cache.delete(__session_key(user_session_id))


def get_feedback(user_session_id, cache):
    session_key = __session_feedback_key(user_session_id)
    feedback = cache.get(session_key)

    return default_if_blank(feedback, 'N.A.')


def set_feedback(user_session_id, feedback, cache):
    session_key = __session_feedback_key(user_session_id)
    cache.set(session_key, feedback)


def __session_key(user_session_id):
    return "session_{}".format(default_if_blank(user_session_id, ''))


def __session_feedback_key(user_session_id):
    return "session__feedback_{}".format(default_if_blank(user_session_id, ''))

import json
from datetime import datetime

from flask import Flask, request
from flask_caching import Cache
from flask_socketio import SocketIO, emit

from cache import get_current_session, clear_current_session
from constants import START_EVENT, END_EVENT, TELEGRAM_USER_ID, AGENT_USER_TYPE, \
    MESSAGE_SOCKET_EVENT, AGENT_SOCKET_EVENT, LIVE_CHAT_SOCKET_EVENT, ONGOING_LIVE_CHAT_TEMPLATE
from dialogflow import process_user_input, detect_intent_via_event
from telegram import send_message
from utils import get_user_id_from_request, get_user_input_from_request

app = Flask(__name__)

config = {
    "CACHE_TYPE": "simple",
    "CACHE_DEFAULT_TIMEOUT": 60 * 20,  # 20 minutes expiry for session ids
}
app.config.from_mapping(config)
cache = Cache(app)
socketio = SocketIO(app)


@socketio.on('connect')
def handle_connect():
    print('Client connected')


@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')


@socketio.on(MESSAGE_SOCKET_EVENT)
def handle_message(data):
    print('Received message: ' + data)
    session = get_current_session(request.sid, cache)

    if data == END_EVENT:
        clear_current_session(request.sid, cache)
        return
    elif session.is_new:
        detect_intent_via_event(session.chat_session_id, START_EVENT)

    emit(MESSAGE_SOCKET_EVENT, process_user_input(session, data, cache))


@socketio.on(LIVE_CHAT_SOCKET_EVENT)
def handle_live_chat(data):
    print('Received message: ' + data)
    send_message(ONGOING_LIVE_CHAT_TEMPLATE.format(request.sid, data))


@app.route('/', methods=['GET'])
def health_check():
    return 'Hello, World!'


@app.route('/webhook', methods=['POST'])
def webhook():
    req_body = request.get_json()
    print('Received webhook: ' + json.dumps(request.get_json()))

    if req_body is None:
        return "ERROR: No request body", 400

    user_id = get_user_id_from_request(req_body)

    if user_id < 1 or not user_id == TELEGRAM_USER_ID:
        return "ERROR: Invalid user id", 400

    user_input = get_user_input_from_request(req_body)
    if len(user_input.split()) < 2:
        send_message("Invalid response. Accepting '<session_id> <reply>'")
        return ''

    session_id = user_input.split()[0]
    if session_id not in socketio.server.manager.rooms["/"].keys():
        send_message("Invalid or expired session id '{}'".format(session_id))
        return ''

    text = user_input[len(session_id) + 1:]

    emit(AGENT_SOCKET_EVENT, __build_response(text),
         namespace="/",
         to=session_id,
         skip_sid=__get_all_other_session_ids_besides(session_id))

    return ''


def __build_response(text):
    return {
        "type": AGENT_USER_TYPE,
        "text": text,
        "date": datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
    }


def __get_all_other_session_ids_besides(target_session_id):
    return list(filter(lambda key: key is not None and not key == target_session_id,
                       socketio.server.manager.rooms["/"].keys()))


if __name__ == "__main__":
    socketio.run(app)

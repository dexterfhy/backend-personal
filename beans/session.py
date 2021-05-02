class Session:
    def __init__(self, socket_sid, chat_sid, is_new):
        self.__socket_session_id = socket_sid
        self.__chat_session_id = chat_sid
        self.__is_new = is_new

    @property
    def socket_session_id(self):
        return self.__socket_session_id

    @property
    def chat_session_id(self):
        return self.__chat_session_id

    @property
    def is_new(self):
        return self.__is_new

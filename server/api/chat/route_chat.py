from server.api.chat.get_history import *
from server.api.chat.chat import *


def join_chat_routes(app):
    create_get_history_route(app)
    create_chat_route(app)

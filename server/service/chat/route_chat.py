from server.service.chat.get_memory import *
from tools.resp import base_resp
from tools.token import *


def join_chat_routes(app):
    create_get_history_route(app)

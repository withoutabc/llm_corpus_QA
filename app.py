import os

from flask import Flask

from dotenv import load_dotenv
from zep_python import ZepClient

from server.api.chat.chat import create_chat_route
from server.api.session.session import create_session_route
from server.api.user.user import create_user_route

load_dotenv()

# 设置环境变量
if __name__ == '__main__':
    app = Flask(__name__)
    create_user_route(app)
    create_chat_route(app)
    create_session_route(app)
    app.run(host='0.0.0.0', port=5000, debug=True)

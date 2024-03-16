from flask import Flask

from dotenv import load_dotenv
from flask_cors import CORS

from server.api.chat.chat import create_chat_route
from server.api.session.session import create_session_route
from server.api.user.user import create_user_route

# 加载环境变量
load_dotenv()

if __name__ == '__main__':
    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    create_user_route(app)
    create_chat_route(app)
    create_session_route(app)
    app.run(threaded=True, debug=True, port=5000, host='0.0.0.0')

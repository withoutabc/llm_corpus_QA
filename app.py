from flask import Flask

from dotenv import load_dotenv

from server.api.chat.chat import create_chat_route
from server.api.session.session import create_session_route
from server.api.user.user import create_user_route

load_dotenv()
app = Flask(__name__)

create_user_route(app)
create_chat_route(app)
create_session_route(app)

if __name__ == '__main__':
    app.run(debug=True)

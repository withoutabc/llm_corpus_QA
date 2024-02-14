from flask import Flask
from server.api.user.route_user import join_user_routes
from server.api.chat.route_chat import join_chat_routes

from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

join_user_routes(app)
join_chat_routes(app)

if __name__ == '__main__':
    app.run(debug=True)

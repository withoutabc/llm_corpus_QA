from flask import Flask
from server.service.user.route_user import join_user_routes

app = Flask(__name__)

join_user_routes(app)

if __name__ == '__main__':
    app.run(debug=True)

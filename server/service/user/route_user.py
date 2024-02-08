# app.py

from flask import Flask
from api_routes import create_hello_route

app = Flask(__name__)

# 导入路由和功能
create_hello_route(app)

if __name__ == '__main__':
    app.run(debug=True)
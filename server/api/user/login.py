from flask import jsonify, request
from tools.error import *
from tools.resp import base_resp
from tools.token import *


def create_login_route(app):
    @app.route('/user/login', methods=['POST'])
    def login():
        try:
            data = request.get_json()
        except KeyError:
            print("KeyError: 'username' not found")
            return jsonify(base_resp(param_error))
        except Exception as e:
            print(f"An error occurred: {e}")
            return jsonify(base_resp(internal_server_error))

        try:
            username = data['username']
            password = data['password']
        except KeyError:
            print("key error")
            return jsonify(base_resp(param_error))
        except Exception as e:
            print(f"An error occurred: {e}")
            return jsonify(base_resp(internal_server_error))
        # 获取user_id
        user_id = 1
        if username == 'admin':
            data = {}
            data['user_id'] = str(user_id)
            data['access_token'] = generate_access_token(user_id)
            data['refresh_token'] = generate_refresh_token(user_id)
            resp = base_resp(success)
            resp['data'] = data
            return jsonify(resp)
        else:
            return jsonify(base_resp(user_not_found))

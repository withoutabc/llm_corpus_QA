from flask import jsonify, request
from tools.error import *
from tools.resp import base_resp
from tools.token import *


def create_refresh_route(app):
    @app.route('/user/refresh', methods=['POST'])
    def refresh():
        try:
            req = request.get_json()
        except KeyError:
            print("KeyError")
            return jsonify(base_resp(param_error))
        except Exception as e:
            print(f"An error occurred: {e}")
            return jsonify(base_resp(internal_server_error))

        try:
            refresh_token = req['refresh_token']
        except KeyError:
            print("key error")
            return jsonify(base_resp(param_error))
        except Exception as e:
            print(f"An error occurred: {e}")
            return jsonify(base_resp(internal_server_error))
        # 验证token
        user_id = verify_refresh_token(refresh_token)
        if user_id:
            print(f"User ID解析成功: {user_id}")
        else:
            return jsonify(base_resp(token_invalid))
        data = {}
        data['user_id'] = user_id
        data['access_token'] = generate_access_token(user_id)
        resp = base_resp(success)
        resp['data'] = data
        return resp

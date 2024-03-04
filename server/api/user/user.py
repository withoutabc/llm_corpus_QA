import os

import shortuuid
from flask import jsonify, request
from zep_python import ZepClient
from zep_python.user import CreateUserRequest

from tools.error import *
from tools.resp import base_resp
from tools.token import *


def create_user_route(app):
    @app.route('/user/register', methods=['POST'])
    def register():
        try:
            req = request.get_json()
            username = req['username']
            password = req['password']
        except Exception as e:
            print(f"An error occurred: {e}")
            return jsonify(base_resp(internal_server_error))

        try:
            client = ZepClient(base_url=os.getenv('ZEP_API_URL'))
            users = client.user.list(cursor=0)
            for user in users:
                if user.first_name == username:
                    return jsonify(base_resp(user_repeated))
        except Exception as e:
            print(f"An error occurred: {e}")
            return jsonify(base_resp(internal_server_error))

        try:
            user_id = shortuuid.uuid()
            user_request = CreateUserRequest(
                user_id=user_id,
                email=" ",
                first_name=username,
                last_name="",
                metadata={"password": password},
            )
            client.user.add(user_request)
        except Exception as e:
            print(f"An error occurred: {e}")
            return jsonify(base_resp(internal_server_error))

        return jsonify(base_resp(success))

    @app.route('/user/login', methods=['POST'])
    def login():
        try:
            data = request.get_json()
            username = data['username']
            password = data['password']
        except KeyError:
            print("KeyError")
            return jsonify(base_resp(param_error))
        except Exception as e:
            print(f"An error occurred: {e}")
            return jsonify(base_resp(internal_server_error))

        try:
            client = ZepClient(base_url=os.getenv('ZEP_API_URL'))
            users = client.user.list(cursor=0)
            for user in users:
                if user.first_name == username:
                    if user.metadata['password'] == password:
                        user_id = user.user_id
                        data = {}
                        data['user_id'] = str(user_id)
                        data['access_token'] = generate_access_token(user_id)
                        data['refresh_token'] = generate_refresh_token(user_id)
                        resp = base_resp(success)
                        resp['data'] = data
                        return jsonify(resp)
                    else:
                        return jsonify(base_resp(wrong_password))
            return jsonify(base_resp(user_not_found))
        except Exception as e:
            print(f"An error occurred: {e}")
            return jsonify(base_resp(internal_server_error))

    @app.route('/user/refresh', methods=['POST'])
    def refresh():
        try:
            req = request.get_json()
            refresh_token = req['refresh_token']
        except KeyError:
            print("KeyError")
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
    @app.route('/hello', methods=['GET'])
    def hello():
        return jsonify(base_resp(success))
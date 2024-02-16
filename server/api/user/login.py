import os

from flask import jsonify, request
from zep_python import ZepClient

from tools.error import *
from tools.resp import base_resp
from tools.token import *


def create_login_route(app):
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
import os

from flask import jsonify, request
from zep_python import ZepClient
from zep_python.user import CreateUserRequest

from tools.error import *
from tools.resp import base_resp

import shortuuid


def create_register_route(app):
    @app.route('/user/register', methods=['GET'])
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

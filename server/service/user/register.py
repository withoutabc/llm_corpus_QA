from flask import jsonify, request
from tools.error import *
from tools.resp import base_resp
from tools.token import *


def create_register_route(app):
    @app.route('/user/register', methods=['GET'])
    def register():
        try:
            req = request.get_json()
        except KeyError:
            print("KeyError")
            return jsonify(base_resp(param_error))
        except Exception as e:
            print(f"An error occurred: {e}")
            return jsonify(base_resp(internal_server_error))

        return {}

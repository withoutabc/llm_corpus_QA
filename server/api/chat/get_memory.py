from flask import request, jsonify
from tools.error import *
from tools.resp import base_resp
from tools.memory import *


# 会话不存在也会返回成功，但是集合为空
def create_get_history_route(app):
    @app.route('/memory', methods=['GET'])
    def get_history_route():
        try:
            req = request.get_json()
        except KeyError:
            print("KeyError")
            return jsonify(base_resp(param_error))
        except Exception as e:
            print(f"An error occurred: {e}")
            return jsonify(base_resp(internal_server_error))

        try:
            session_id = req['session_id']
            # 验证 session_id 是否为字符串
            if not isinstance(session_id, str):
                return jsonify(base_resp(param_error))
        except KeyError:
            print("key error")
            return jsonify(base_resp(param_error))
        except Exception as e:
            print(f"An error occurred: {e}")
            return jsonify(base_resp(internal_server_error))

        history = get_history(session_id)
        if history == None:
            return jsonify(base_resp(session_not_found))
        resp = base_resp(success)
        resp['data'] = history
        return jsonify(resp)

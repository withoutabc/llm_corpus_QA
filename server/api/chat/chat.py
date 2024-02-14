from flask import request

from server.service.chain import get_chain
from tools.error import *
from tools.resp import base_resp
from tools.memory import *


def create_chat_route(app):
    @app.route('/chat', methods=['POST'])
    def chat_route():
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
            category = req['category']
            question = req['content']
            # 验证 session_id 是否为字符串
            if not isinstance(session_id, str):
                return jsonify(base_resp(param_error))
        except KeyError:
            print("key error")
            return jsonify(base_resp(param_error))
        except Exception as e:
            print(f"An error occurred: {e}")
            return jsonify(base_resp(internal_server_error))

        chain = get_chain(session_id, category)
        res = chain.invoke(
            input={"query": question}
        )

        resp = base_resp(success)
        data = {"answer": res['result']}
        resp['data'] = data
        return jsonify(resp)

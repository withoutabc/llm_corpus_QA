from flask import request

from server.service.chain import get_chain
from server.service.history import transfer_history, get_zep_chat_history
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

        zep_history = get_zep_chat_history(session_id)

        history = transfer_history(zep_history)

        res = chain.invoke(
            input={"question": question, "chat_history": history}
        )

        zep_history.add_user_message(question)
        zep_history.add_ai_message(res['answer'])

        resp = base_resp(success)
        data = {"answer": res['answer']}
        resp['data'] = data
        return jsonify(resp)

from server.llm.persist.retrieval import get_retrieval
from tools.memory import *
from flask import request, jsonify
from tools.error import *
from tools.resp import base_resp
from tools.memory import *
from tools.history import get_zep_chat_history


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

        persist_dictionary = './../../llm/data_base/knowledge_db/'
        retrieval = get_retrieval(persist_dictionary)



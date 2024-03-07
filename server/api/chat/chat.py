from flask import request, jsonify

from server.service.chain import get_chain
from server.service.history import transfer_history, get_zep_chat_history
from tools.error import *
from tools.resp import base_resp
from tools.token import verify_access_token


def create_chat_route(app):
    @app.route('/chat', methods=['POST'])
    def chat_route():
        # 获取Authorization头部信息
        authorization_header = request.headers.get('Authorization')
        # 检查是否有Bearer Token
        if not authorization_header or not authorization_header.startswith('Bearer '):
            return jsonify(base_resp(unauthorized_error))
        # 提取Bearer Token
        access_token = authorization_header.split(' ')[1]
        # 验证访问令牌
        user_id_from_access_token = verify_access_token(access_token)
        if user_id_from_access_token:
            print(f"User ID解析成功: {user_id_from_access_token}")
        else:
            return jsonify(base_resp(token_invalid))

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

        chain = get_chain(category)

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

    @app.route('/history', methods=['GET'])
    def get_history_route():
        # 获取Authorization头部信息
        authorization_header = request.headers.get('Authorization')
        # 检查是否有Bearer Token
        if not authorization_header or not authorization_header.startswith('Bearer '):
            return jsonify(base_resp(unauthorized_error))
        # 提取Bearer Token
        access_token = authorization_header.split(' ')[1]
        # 验证访问令牌
        user_id_from_access_token = verify_access_token(access_token)
        if user_id_from_access_token:
            print(f"User ID解析成功: {user_id_from_access_token}")
        else:
            return jsonify(base_resp(token_invalid))
        try:
            req = request.get_json()
            session_id = req['session_id']
            # 验证 session_id 是否为字符串
            if not isinstance(session_id, str):
                return jsonify(base_resp(param_error))
        except KeyError:
            print("KeyError")
            return jsonify(base_resp(param_error))
        except Exception as e:
            print(f"An error occurred: {e}")
            return jsonify(base_resp(internal_server_error))

        try:
            history = get_zep_chat_history(session_id)
            if history == None:
                return jsonify(base_resp(session_not_found))
            resp = base_resp(success)
            history_ = []
            for message in history.zep_messages:
                history_.append(message.to_dict())
            resp['data'] = history_
            return jsonify(resp)
        except Exception as e:
            print(f"An error occurred: {e}")
            return jsonify(base_resp(internal_server_error))

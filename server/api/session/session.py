import asyncio
import os
import uuid

from flask import request, jsonify
from zep_python import ZepClient, Session

from tools.error import *
from tools.resp import base_resp
from tools.token import verify_access_token


def create_session_route(app):
    @app.route('/session', methods=['POST'])
    def create_session_route():
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
            data = request.get_json()
            category = data['category']
        except KeyError:
            print("KeyError")
            return jsonify(base_resp(param_error))
        except Exception as e:
            print(f"An error occurred: {e}")
            return jsonify(base_resp(internal_server_error))

        try:
            asyncio.run(create_session_async(user_id_from_access_token, category))
        except Exception as e:
            print(f"An error occurred: {e}")
            return jsonify(base_resp(internal_server_error))

        return jsonify(base_resp(success))

    @app.route('/session', methods=['GET'])
    def get_session_route():
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
            client = ZepClient(base_url=os.getenv('ZEP_API_URL'))
            sessions = client.user.get_sessions(user_id_from_access_token)
            sessions_ = []
            for session in sessions:
                sessions_.append(session)
        except Exception as e:
            print(f"An error occurred: {e}")
            return jsonify(base_resp(internal_server_error))

        return jsonify(sessions_)

    @app.route('/session', methods=['DELETE'])
    def delete_session_route():
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
            data = request.get_json()
            session_id = data['session_id']
        except KeyError:
            print("KeyError")
            return jsonify(base_resp(param_error))
        except Exception as e:
            print(f"An error occurred: {e}")
            return jsonify(base_resp(internal_server_error))

        try:
            asyncio.run(delete_session_async(session_id))
        except Exception as e:
            print(f"An error occurred: {e}")
            return jsonify(base_resp(internal_server_error))

        return jsonify(success)


async def create_session_async(user_id: str, category: str):
    async with ZepClient(base_url=os.getenv('ZEP_API_URL')) as client:
        session_id = uuid.uuid4().hex
        session = Session(
            session_id=session_id,
            user_id=user_id,
            metadata={'category': category}
        )
        await client.memory.aadd_session(session)


async def delete_session_async(session_id: str):
    async with ZepClient(base_url=os.getenv('ZEP_API_URL')) as client:
        await client.memory.adelete_memory(session_id)

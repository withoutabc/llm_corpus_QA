import asyncio
import os
import openai
from flask import jsonify
from langchain.memory import ConversationBufferMemory
from zep_python import NotFoundError, ZepClient
from dotenv import load_dotenv

load_dotenv()
ZEP_API_URL = os.getenv('ZEP_API_URL')
openai.api_key = os.getenv('OPENAI_API_KEY')
openai.base_url = os.getenv('OPENAI_BASE_URL')
zep_api_key = openai.api_key
session_id = "386bcc25-b9d2-409f-818d-eb14c45f4d49"

async def get_memory_async(session_id: str):
    history = []
    async with ZepClient(base_url=ZEP_API_URL, api_key=zep_api_key) as client:
        try:
            memory = await client.memory.aget_memory(session_id)
            for message in memory.messages:
                history.append(message.to_dict())
        except NotFoundError:
            return None, None
        except Exception as e:
            return None, None
    return history, memory




def get_history(session_id):
    history, memory = asyncio.run(get_memory_async(session_id))
    if history == None or memory == None:
        return None
    return history

# def get_memory(session_id):
#     history, memory = asyncio.run(get_memory_async(session_id))
#     if history == None or memory == None:
#         return None
#     return memory


# def history_transfer(session_id: str):
#     history = get_history(session_id)
#     # 初始化 ConversationBufferMemory
#     memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
#     # 遍历历史记录并添加到 ConversationBufferMemory
#     for entry in history:
#         role = entry['role']
#         content = entry['content']
#         if role == 'human':
#             memory.chat_memory.add_user_message(content)
#         elif role == 'ai':
#             memory.chat_memory.add_ai_message(content)
#     return memory

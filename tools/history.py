import os
import openai
from dotenv import load_dotenv
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import ZepChatMessageHistory


def get_zep_chat_history(session_id: str):
    chat_history = ZepChatMessageHistory(
        session_id=session_id,
        url=os.getenv('ZEP_API_URL'),
        # api_key=os.getenv('OPENAI_API_KEY'),

    )
    return chat_history


memory = ConversationBufferMemory(
    memory_key="chat_history",
    chat_memory=get_zep_chat_history('5d691c6d-fbd6-4237-a9e9-dab260d8410b')
)

print(memory.chat_memory)

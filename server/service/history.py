import os

from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import ZepChatMessageHistory


def get_zep_chat_history(session_id: str):
    zep_chat_history = ZepChatMessageHistory(
        session_id=session_id,
        url=os.getenv('ZEP_API_URL'),
        # api_key=os.getenv('OPENAI_API_KEY'),

    )
    return zep_chat_history


def get_conversation_buffer_memory(session_id: str):
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        chat_memory=get_zep_chat_history(session_id)
    )
    return memory

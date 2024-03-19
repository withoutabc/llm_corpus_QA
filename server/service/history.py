import os

from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import ZepChatMessageHistory


def get_zep_chat_history(session_id: str):
    zep_chat_history = ZepChatMessageHistory(
        session_id=session_id,
        url=os.getenv('ZEP_API_URL'),
        # api_key=os.getenv('OPENAI_API_KEY'),
    )
    # print(zep_chat_history.zep_messages)
    history = []
    for message in zep_chat_history.zep_messages:
        if message.metadata['delete_at'] != "":
            continue
        if message.role == 'human':
            history.append("Human:" + message.content)
        if message.role == 'ai':
            history.append("Assistant:" + message.content)
    return zep_chat_history, "\n".join(history)

# def get_conversation_buffer_memory(session_id: str):
#     memory = ConversationBufferMemory(
#         memory_key="chat_history",
#         chat_memory=get_zep_chat_history(session_id)
#     )
#     return memory


# def transfer_history(chat_history: ZepChatMessageHistory):
#     history = []
#     for i in range(0, len(chat_history.zep_messages), 2):
#         pair = (chat_history.zep_messages[i].to_dict()['content'],
#                 chat_history.zep_messages[i + 1].to_dict()['content'] if i + 1 < len(
#                     chat_history.zep_messages) else None)
#         history.append(pair)
#     return history

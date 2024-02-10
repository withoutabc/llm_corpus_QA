import os
import openai
from tools.history import get_zep_chat_history
from langchain.prompts import (
    ChatPromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from langchain_community.chat_message_histories import ZepChatMessageHistory
from dotenv import load_dotenv

load_dotenv()
ZEP_API_URL = os.getenv('ZEP_API_URL')
openai.api_key = os.getenv('OPENAI_API_KEY')
openai.base_url = os.getenv('OPENAI_BASE_URL')
zep_api_key = openai.api_key

session_id = "2edfb87eaceb4d70bda5c91db2f9922a"


def get_prompt(session_id: str):
    return


def deal_with_history(session_id: str):
    history = get_zep_chat_history(session_id)
    if len(history.messages) == 0:
        return []
    else:
        msgs = history.messages


    dealt = deal_with_history(session_id)

    print(dealt)

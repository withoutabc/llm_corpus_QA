import os

from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
)

from langchain.chains import ConversationalRetrievalChain

from server.service.chain import get_chain
from server.service.history import get_zep_chat_history
from server.service.load import get_retrieval

load_dotenv()
ZEP_API_URL = os.getenv('ZEP_API_URL')

session_id=''
chain = get_chain(session_id,'type')
question = '请论述主成分分析'

res = chain.invoke({"question": question})

print(res)

import os

import openai
from langchain.chains import RetrievalQA
from langchain_community.chat_message_histories import ZepChatMessageHistory
from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
import openai
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain_community.vectorstores.chroma import Chroma

from langchain_openai import OpenAI
from langchain.chains import ConversationalRetrievalChain, LLMChain
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv

load_dotenv()
ZEP_API_URL = os.getenv('ZEP_API_URL')
openai.api_key = os.getenv('OPENAI_API_KEY')
openai.base_url = os.getenv('OPENAI_BASE_URL')
zep_api_key = openai.api_key


# # 创建 ChatOpenAI 实例
# llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
#
# template = "You are a helpful assistant.\n"
# system_message_prompt = SystemMessagePromptTemplate.from_template(template)
# human_template = "{question}"
# human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
# chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
#
# # 定义 Embeddings
# embedding = OpenAIEmbeddings()
#
# # 向量数据库持久化路径
# persist_directory = '../data_base/vector_db/chroma'
#
# # 加载数据库
# vectordb = Chroma(
#     persist_directory=persist_directory,  # 允许我们将 persist_directory 目录保存到磁盘上
#     embedding_function=embedding
# )
#
# load_dotenv()
# openai_api_key = os.getenv('OPENAI_API_KEY')
#

#
# zep_chat_history = ZepChatMessageHistory(
#     session_id=session_id,
#     url="http://localhost:8000",
#     api_key=os.getenv('OPENAI_API_KEY'),
# )
#
# qa_chain = RetrievalQA.from_chain_type(
#     ChatOpenAI(model="gpt-3.5-turbo", api_key=openai_api_key),
#     retriever=vectordb.as_retriever()
# )
# prompt = ChatPromptTemplate.from_messages(
#     [
#         ("system", "You're an assistant."),
#         MessagesPlaceholder(variable_name="chat_history"),
#         ("human", "{query}"),
#     ]
# )
#
# conversation_retrieval_chain = ConversationalRetrievalChain.from_llm(
#     llm,
#     # condense_question_prompt=chat_prompt,
#     retriever=vectordb.as_retriever(),
#     # condense_question_llm=ChatOpenAI(temperature=0, model='gpt-3.5-turbo'),
#     # memory=memory
# )
#
# chain = prompt | conversation_retrieval_chain
#
# chain_with_history = RunnableWithMessageHistory(
#     chain,
#     lambda session_id: zep_chat_history,
#     # input_messages_key="question",
#     history_messages_key="chat_history",
# )
#
# x = {"query": "What's its inverse?"}
#
# chain_with_history.invoke(
#     input=x,
#     config={"configurable": {"session_id": session_id}},
# )
#
# print(zep_chat_history)


def get_zep_chat_history(session_id: str):
    chat_history = ZepChatMessageHistory(
        session_id=session_id,
        url=os.getenv('ZEP_API_URL'),
        api_key=os.getenv('OPENAI_API_KEY'),
    )
    return chat_history

# chat_history=get_zep_chat_history()
#
# print(type(chat_history))
#
# print(chat_history.messages[0])
#
# print(type(chat_history.messages[0]))

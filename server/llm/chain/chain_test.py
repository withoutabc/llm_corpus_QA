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
from server.llm.persist.retrieval import *

load_dotenv()
ZEP_API_URL = os.getenv('ZEP_API_URL')
openai.api_key = os.getenv('OPENAI_API_KEY')
openai.base_url = os.getenv('OPENAI_BASE_URL')
zep_api_key = openai.api_key

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
memory.chat_memory.add_user_message("主成份分析是什么")
memory.chat_memory.add_ai_message(
    "主成分分析（Principal Component Analysis，PCA）是一种常用的降维技术，用于将高维数据转换为低维数据，同时保留数据的主要特征。它通过线性变换将原始数据投影到一个新的坐标系中，使得投影后的数据具有最大的方差。这样做的目的是减少数据的维度，同时尽可能地保留数据的信息。\n\n主成分分析可以用于数据可视化、数据压缩、特征提取等领域。在数据可视化中，主成分分析可以将高维数据映射到二维或三维空间中，方便我们观察和理解数据的分布情况。在数据压缩中，主成分分析可以将高维数据转换为低维数据，从而减少存储空间和计算复杂度。在特征提取中，主成分分析可以提取出数据中最重要的特征，用于后续的分类、聚类等任务。")


template = "You are a helpful assistant.\n"
system_message_prompt = SystemMessagePromptTemplate.from_template(template)

chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt])

# 定义持久化路径
persist_directory = '../data_base/vector_db/chroma'
retriever = get_retrieval(persist_directory)

history = get_zep_chat_history("386bcc25-b9d2-409f-818d-eb14c45f4d49")
print(history.messages)

conversation_retrieval_chain = ConversationalRetrievalChain.from_llm(
    llm=ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0),
    # condense_question_prompt=chat_prompt,
    retriever=retriever,
    # condense_question_llm=ChatOpenAI(temperature=0, model='gpt-3.5-turbo'),
    memory=history
)
question = '请你重述上一句话'

res = conversation_retrieval_chain.invoke({"question": question})

print(memory)

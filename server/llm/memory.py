import asyncio
import os
import uuid
from langchain.embeddings.openai import OpenAIEmbeddings
from uuid import uuid4
from langchain.chat_models import ChatOpenAI
import openai
from dotenv import load_dotenv, find_dotenv
from langchain.agents import AgentType, Tool, initialize_agent
from langchain.memory import ZepMemory
from langchain.retrievers import ZepRetriever
from langchain.schema import AIMessage, HumanMessage
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.vectorstores.chroma import Chroma
from langchain_openai import OpenAI
from zep_python import NotFoundError, ZepClient
from dotenv import load_dotenv, find_dotenv  # 导入dotenv库

load_dotenv()
ZEP_API_URL = os.getenv('ZEP_API_URL')
openai.api_key = os.getenv('OPENAI_API_KEY')
openai.base_url = os.getenv('OPENAI_BASE_URL')
zep_api_key = openai.api_key


async def get_memory_async():
    history = []
    async with ZepClient(base_url=ZEP_API_URL, api_key=zep_api_key) as client:
        try:
            memory = await client.memory.aget_memory('5d691c6d-fbd6-4237-a9e9-dab260d8410b')
            for message in memory.messages:
                history.append(message.to_dict())
        except NotFoundError:
            print("Memory not found")
    return history, memory


def get_history():
    return asyncio.run(get_memory_async())

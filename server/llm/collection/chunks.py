import openai
from langchain_community.vectorstores.zep import ZepVectorStore
from zep_python.document import Document

from server.llm.collection.load import load
from langchain.text_splitter import RecursiveCharacterTextSplitter

import os

from zep_python import ZepClient
from dotenv import load_dotenv

load_dotenv()
openai.base_url = os.getenv('OPENAI_BASE_URL')
zep_api_key = os.getenv('OPENAI_API_KEY')
zep_base_url = os.getenv('ZEP_API_URL')

client = ZepClient(base_url=zep_base_url, api_key=zep_api_key)

collection_name = "babbagedocs"
collection = client.document.get_collection(collection_name)

vectorstore = ZepVectorStore(collection_name, api_url=zep_base_url, api_key=zep_api_key)

split_docs = load()

uuids = vectorstore.add_documents(split_docs)

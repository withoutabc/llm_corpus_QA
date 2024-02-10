import time

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

collection_name = "babbagedocs"
client = ZepClient(base_url=zep_base_url, api_key=zep_api_key)

while True:
    c = client.document.get_collection(collection_name)
    print(
        "Embedding status: "
        f"{c.document_embedded_count}/{c.document_count} documents embedded"
    )
    time.sleep(1)
    if c.status == "ready":
        break

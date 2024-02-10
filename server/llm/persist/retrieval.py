from langchain.embeddings.openai import OpenAIEmbeddings
from tools.history import *

load_dotenv()
ZEP_API_URL = os.getenv('ZEP_API_URL')
openai.api_key = os.getenv('OPENAI_API_KEY')
openai.base_url = os.getenv('OPENAI_BASE_URL')
zep_api_key = openai.api_key


def load_db(persist_directory):
    # 定义 Embeddings
    embedding = OpenAIEmbeddings()
    # 加载数据库
    vectordb = Chroma(
        persist_directory=persist_directory,  # 允许我们将 persist_directory 目录保存到磁盘上
        embedding_function=embedding
    )
    return vectordb


def get_retrieval(persist_directory):
    return load_db(persist_directory).as_retriever()

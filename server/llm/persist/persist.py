# 首先实现基本配置
import openai
from langchain.vectorstores import Chroma  # 导入Chroma向量存储库
from langchain.document_loaders import PyMuPDFLoader  # 导入PyMuPDFLoader文档加载库
from langchain.text_splitter import RecursiveCharacterTextSplitter  # 导入RecursiveCharacterTextSplitter文本拆分库
from langchain.document_loaders import UnstructuredMarkdownLoader  # 导入UnstructuredMarkdownLoader文档加载库
from langchain.document_loaders import UnstructuredFileLoader  # 导入UnstructuredFileLoader文档加载库

from langchain.embeddings.openai import OpenAIEmbeddings  # 导入OpenAIEmbeddings嵌入库

from langchain.llms import OpenAI  # 导入OpenAI LLMS（Language Model Microservice）库
import time

# 使用前配置自己的 api 到环境变量中
import os  # 导入os库

from dotenv import load_dotenv, find_dotenv  # 导入dotenv库

_ = load_dotenv(find_dotenv())  # 加载环境变量文件
# 设置OpenAI的API密钥
os.environ['OPENAI_API_KEY'] = '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'
openai.api_key = os.environ['OPENAI_API_KEY']
# sk-FT0qSwD4e5NsJWnr2bAaA30b0f3f4d1cBd5712Dd6e958010
# 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 openai
os.environ["HTTP_PROXY"] = "http://127.0.0.1:7890"
os.environ["HTTPS_PROXY"] = "http://127.0.0.1:7890"
# 指定 PDF 文件所在的文件夹路径
folder_path = "../data_base/knowledge_db/pdf/"

# 获取文件夹中的所有文件名
files = os.listdir(folder_path)

# 创建加载器列表
loaders = []

# 遍历文件列表
for one_file in files:
    # 根据文件路径创建 PyMuPDFLoader 加载器
    loader = PyMuPDFLoader(os.path.join(folder_path, one_file))

    # 将加载器添加到列表中
    loaders.append(loader)

# 创建文档列表
docs = []

# 遍历加载器列表
for loader in loaders:
    # 加载文档并将其添加到文档列表中
    docs.extend(loader.load())

# 指定 Markdown 文件所在的文件夹路径
folder_path = "../data_base/knowledge_db/md/"

# 获取文件夹中的所有文件名
files = os.listdir(folder_path)

# 创建加载器列表
loaders = []

# 遍历文件列表
for one_file in files:
    # 根据文件路径创建 UnstructuredMarkdownLoader 加载器
    loader = UnstructuredMarkdownLoader(os.path.join(folder_path, one_file))

    # 将加载器添加到列表中
    loaders.append(loader)

# 创建文档列表
docs = []

# 遍历加载器列表
for loader in loaders:
    # 加载文档并将其添加到文档列表中
    docs.extend(loader.load())

# 切分文档
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=150)
split_docs = text_splitter.split_documents(docs)

# 定义 Embeddings
embedding = OpenAIEmbeddings()

# 定义持久化路径
persist_directory = '../data_base/vector_db/chroma'

# 加载数据库
vectordb = Chroma.from_documents(
    documents=split_docs,
    embedding=embedding,
    persist_directory=persist_directory  # 允许我们将persist_directory目录保存到磁盘上
)

# 向量数据库持久化
vectordb.persist()
import os

from langchain_community.embeddings import QianfanEmbeddingsEndpoint
from langchain_community.vectorstores.chroma import Chroma
from server.service.split import split_docs

from server.service.load import load_docs
from dotenv import load_dotenv, find_dotenv


def persist_vector_db(category: str, s_docs):
    # 定义 Embeddings
    embedding = QianfanEmbeddingsEndpoint(
        streaming=True,
        model="Embedding-V1",
        chunk_size=16,
    )
    base_directory = '../../../data_base/'
    # 定义持久化路径
    persist_directory = os.path.join(base_directory, category)

    # 加载数据库
    vectordb = Chroma.from_documents(
        documents=split_docs(s_docs),
        embedding=embedding,
        persist_directory=persist_directory  # 允许我们将persist_directory目录保存到磁盘上
    )

    # 向量数据库持久化
    vectordb.persist()


if __name__ == '__main__':
    _ = load_dotenv(find_dotenv())
    docs_dict = load_docs()
    for category, docs in docs_dict.items():
        # if category not in ['Chinese_medicine_physique','device','medicine','cancer','cardiology',]:
        print(docs)
        persist_vector_db(category, docs)

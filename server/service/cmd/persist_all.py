import os
import time

from langchain_community.embeddings import QianfanEmbeddingsEndpoint
from langchain_community.vectorstores.chroma import Chroma
from langchain_core.documents import Document

from server.service.split import split_docs

from server.service.load import load_docs
from dotenv import load_dotenv, find_dotenv


def persist_vector_db_all(docs_dict):
    # 定义 Embeddings
    embedding = QianfanEmbeddingsEndpoint(
        streaming=True,
        model="Embedding-V1",
        chunk_size=16,
    )
    base_directory = '../../../data_base/'
    # 定义持久化路径
    persist_directory = os.path.join(base_directory, "common")
    doc = Document(page_content="无", metadata={"page": "1"})
    vectordb = Chroma.from_documents(
        documents=split_docs(([doc])),
        collection_name="common",
        embedding=embedding,
        persist_directory=persist_directory,  # 将persist_directory目录保存到磁盘上
    )
    # 记录正确数和错误数
    right = 0
    error = 0
    for i, docs in docs_dict.items():
        for doc in docs:
            if doc.page_content == '':
                continue
            # 加载数据库
            try:
                vectordb.add_documents(documents=split_docs(([doc])))
            except Exception as e:
                error = error + 1
                print(doc)
                print(f"--------------------------------------------\n"
                      f"An error occured: {e}\n"
                      f"--------------------------------------------")
                time.sleep(5)
                continue
            right = right + 1

    print(f"right:{right}")
    print(f"error:{error}")
    print("向量数据库持久化中...")
    vectordb.persist()


if __name__ == '__main__':
    _ = load_dotenv(find_dotenv())
    docs_dict = load_docs()
    # print(docs_dict)
    persist_vector_db_all(docs_dict)

import os
import time

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
    right = 0
    error = 0
    for doc in s_docs:
        if doc.page_content == '':
            continue
        # 加载数据库
        try:
            vectordb = Chroma.from_documents(
                documents=split_docs([(doc)]),
                embedding=embedding,
                persist_directory=persist_directory  # 允许我们将persist_directory目录保存到磁盘上
            )
            # 向量数据库持久化
            vectordb.persist()
        except Exception as e:
            error = error + 1
            print(doc)
            print(f"An error occured: {e}")
            time.sleep(5)
            continue
        right = right + 1
    print(f"right:{right}")
    print(f"error:{error}")


if __name__ == '__main__':
    _ = load_dotenv(find_dotenv())
    docs_dict = load_docs()
    # print(docs_dict)
    cat = input("输入要进行embedding的种类:")
    persist_vector_db(cat, docs_dict[cat])

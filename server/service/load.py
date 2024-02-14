from langchain.vectorstores import Chroma
from langchain.document_loaders import PyMuPDFLoader
from langchain.document_loaders import UnstructuredMarkdownLoader
from langchain.document_loaders import TextLoader
from langchain.document_loaders import UnstructuredFileLoader
from langchain_community.embeddings import QianfanEmbeddingsEndpoint
import os


def load_docs():
    base_path = '../../../knowledge_db/'
    dirs = os.listdir(base_path)
    # print(dirs)

    docs_dict = {}
    for dir in dirs:
        # 创建加载器列表
        loaders = []
        # 创建文档列表
        docs = []
        # 指定 PDF 文件所在的文件夹路径
        category_path = os.path.join(base_path, dir)
        # print(f'category_path:{category_path}')
        folder_paths = os.listdir(category_path)
        for folder_path in folder_paths:
            # 获取文件夹中的所有文件名
            # print(f'folder_path:{folder_path}')
            file_path = os.path.join(category_path, folder_path)
            files = os.listdir(file_path)
            # print(f'file_path:{file_path}')
            if folder_path == 'pdf':
                # 遍历文件列表
                for one_file in files:
                    # print(os.path.join(file_path, one_file))
                    # 根据文件路径创建 PyMuPDFLoader 加载器
                    loader = PyMuPDFLoader(os.path.join(file_path, one_file))

                    # 将加载器添加到列表中
                    loaders.append(loader)

                # 遍历加载器列表
                for loader in loaders:
                    # 加载文档并将其添加到文档列表中
                    docs.extend(loader.load())

            elif folder_path == 'md':
                # 遍历文件列表
                for one_file in files:
                    # 根据文件路径创建 UnstructuredMarkdownLoader 加载器
                    loader = UnstructuredMarkdownLoader(os.path.join(file_path, one_file))

                    # 将加载器添加到列表中
                    loaders.append(loader)

                # 遍历加载器列表
                for loader in loaders:
                    # 加载文档并将其添加到文档列表中
                    docs.extend(loader.load())

            elif folder_path == 'txt':
                for one_file in files:
                    # 根据文件路径创建 UnstructuredMarkdownLoader 加载器
                    loader = TextLoader(os.path.join(file_path, one_file))

                    # 将加载器添加到列表中
                    loaders.append(loader)
                # 遍历加载器列表
                for loader in loaders:
                    # 加载文档并将其添加到文档列表中
                    docs.extend(loader.load())

        docs_dict[dir] = docs
    return docs_dict


def load_db(category: str):
    base_directory = '../../data_base/'
    persist_directory = os.path.join(base_directory, category)
    # 定义 Embeddings
    embedding = QianfanEmbeddingsEndpoint(
        streaming=True,
        model="Embedding-V1",
    )
    # 加载数据库
    vectordb = Chroma(
        persist_directory=persist_directory,  # 允许我们将 persist_directory 目录保存到磁盘上
        embedding_function=embedding
    )
    return vectordb


def get_retrieval(category: str):
    return load_db(category).as_retriever()

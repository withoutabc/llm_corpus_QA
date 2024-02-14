from langchain.text_splitter import RecursiveCharacterTextSplitter

def split_docs(docs):
    # 切分文档
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=150)
    split_docs = text_splitter.split_documents(docs)
    return split_docs

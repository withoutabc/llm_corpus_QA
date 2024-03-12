from langchain.chains import ConversationalRetrievalChain
from langchain_community.chat_models.tongyi import ChatTongyi
from server.service.load import get_retrieval


def get_chain(category: str):
    llm = ChatTongyi(
        model="qwen-max",
        streaming=True
    )

    retrieval = get_retrieval(category)
    # 声明一个检索式问答链
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm,
        chain_type="stuff",
        retriever=retrieval,
        verbose=True,
    )
    return qa_chain

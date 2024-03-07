from langchain.chains import ConversationalRetrievalChain, RetrievalQA

from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import PromptTemplate

from server.service.load import get_retrieval
from server.service.history import get_conversation_buffer_memory


def get_chain(category: str):
    llm = ChatTongyi(
        model="qwen-max",
    )

    retrieval = get_retrieval(category)

    # 声明一个检索式问答链
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm,
        chain_type="stuff",
        retriever=retrieval,
        verbose=True
        # get_chat_history=get_chat_history
    )

    return qa_chain

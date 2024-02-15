from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain_community.chat_models import QianfanChatEndpoint
from langchain_core.prompts import PromptTemplate

from server.service.load import get_retrieval
from server.service.history import get_conversation_buffer_memory


def get_chain(session_id: str, category: str):
    llm = QianfanChatEndpoint(
        streaming=True,
        model="ERNIE-Bot",
    )

    retrieval = get_retrieval(category)

    # 声明一个检索式问答链
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm,
        retriever=retrieval,
        # get_chat_history=get_chat_history
    )

    return qa_chain

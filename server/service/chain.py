from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain_community.chat_models import QianfanChatEndpoint

from server.service.load import get_retrieval
from server.service.history import get_conversation_buffer_memory


def get_chain(session_id: str, category: str):
    llm = QianfanChatEndpoint(
        streaming=True,
        model="ERNIE-Bot",
    )

    retrieval = get_retrieval(category)

    memory = get_conversation_buffer_memory(session_id)

    # 声明一个检索式问答链
    qa_chain = RetrievalQA.from_llm(
        llm,
        retriever=retrieval,
        memory=memory,
        # get_chat_history=get_chat_history
    )

    return qa_chain

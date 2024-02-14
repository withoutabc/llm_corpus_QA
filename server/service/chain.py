from langchain.chains import ConversationalRetrievalChain
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

    # 声明一个对话检索式问答链
    conversation_qa_chain = ConversationalRetrievalChain.from_llm(
        llm,
        retriever=retrieval,
        memory=memory
    )

    return conversation_qa_chain

import queue
import threading

from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain_community.chat_models import QianfanChatEndpoint
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.callbacks import StreamingStdOutCallbackHandler

from server.service.load import get_retrieval


class ThreadedGenerator:
    def __init__(self):
        self.queue = queue.Queue()

    def __iter__(self):
        return self

    def __next__(self):
        item = self.queue.get()
        if item is StopIteration: raise item
        return item

    def send(self, data):
        self.queue.put(data)

    def close(self):
        self.queue.put(StopIteration)


class ChainStreamHandler(StreamingStdOutCallbackHandler):
    def __init__(self, gen):
        super().__init__()
        self.gen = gen

    def on_llm_new_token(self, token: str, **kwargs):
        self.gen.send(token)


def llm_thread(g, cat, question):
    try:
        llm = QianfanChatEndpoint(
            streaming=True,
            model="ERNIE-Bot",
            callbacks=[ChainStreamHandler(g)]
        )
        chain = RetrievalQA.from_llm(
            llm,
            retriever=get_retrieval(cat),
            verbose=True,
        )
        chain({"query": question})
    finally:
        g.close()


def chain(cat, question):
    g = ThreadedGenerator()
    threading.Thread(target=llm_thread, args=(g, cat, question)).start()
    return g

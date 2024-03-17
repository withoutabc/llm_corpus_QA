import asyncio
import queue
import threading

from langchain.chains import ConversationalRetrievalChain, LLMChain
from langchain_community.chat_models import QianfanChatEndpoint
from langchain_core.callbacks import StreamingStdOutCallbackHandler
from langchain_core.prompts import PromptTemplate

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


async def llm_async_operation(g, cat, question, history):
    try:
        template = (
            "Combine the chat history and follow up question into "
            "a standalone question. Chat History: {chat_history}"
            "Follow up question: {question}"
            "A standalone question in Chinese:"
        )
        prompt = PromptTemplate.from_template(template)
        llm = QianfanChatEndpoint(
            streaming=False,
            model="ERNIE-Bot",
        )
        q_gen_chain = LLMChain(llm=llm, prompt=prompt)
        res = q_gen_chain.invoke({"chat_history": history, "question": question})
        q_gen = res['text']
        print(q_gen)
        QA_CHAIN_PROMPT = PromptTemplate(input_variables=["context", "question"],
                                         template=template)
        llm.streaming = True
        llm.callbacks = [ChainStreamHandler(g)]
        chain = ConversationalRetrievalChain.from_llm(
            llm,
            chain_type='stuff',
            retriever=get_retrieval(cat),
        )
        chain({"question": q_gen, "chat_history": []})
    finally:
        g.close()


def llm_thread(g, cat, question, history):
    asyncio.run(llm_async_operation(g, cat, question, history))


def chain(cat, question, history):
    g = ThreadedGenerator()
    threading.Thread(target=llm_thread, args=(g, cat, question, history)).start()
    return g

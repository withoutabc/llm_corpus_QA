import queue
import threading

from dotenv import load_dotenv
from flask import Flask, request, Response
from flask_cors import CORS
from langchain.chains import ConversationalRetrievalChain
from langchain_community.chat_models import QianfanChatEndpoint
from langchain_core.output_parsers import StrOutputParser

# 加载环境变量
load_dotenv()
from server.service.load import get_retrieval
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

app = Flask(__name__)
CORS(app, supports_credentials=True)


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


def llm_thread(g, question, chat_history):
    try:
        llm = QianfanChatEndpoint(
            callbacks=[ChainStreamHandler(g)],
            streaming=True,
            model="ERNIE-Bot",
        )
        chain = ConversationalRetrievalChain.from_llm(
            llm,
            chain_type="stuff",
            retriever=get_retrieval('food'),
            verbose=True,
            # get_chat_history=get_chat_history
        )
        chain({"question": question, "chat_history": chat_history})
    finally:
        g.close()


def chain(question, chat_history):
    g = ThreadedGenerator()
    threading.Thread(target=llm_thread, args=(g, question, chat_history)).start()
    return g


def process_data(data):
    global answer
    # 对总体答案进行操作的逻辑
    # ...
    answer = data


@app.route('/chain', methods=['POST'])
def _chain():
    question = '重庆有哪些好玩的地方,100字以上'
    response = Response(chain(question, ()), mimetype='text/event-stream')
    return response


@app.route('/')
def index():
    # just for the example, html is included directly, move to .html file
    return Response('''
<!DOCTYPE html>
<html>
<head><title>Flask Streaming Langchain Example</title></head>
<body>
    <form id="form">
        <input name="prompt" value="write a short koan story about seeing beyond"/>
        <input type="submit"/>
    </form>
    <div id="output" value="xx" ></div>
    <script>
        const formEl = document.getElementById('form');
        const outputEl = document.getElementById('output');
        let aborter = new AbortController();
        async function run() {
            aborter.abort();  // cancel previous request
            outputEl.innerText = '';
            aborter = new AbortController();
            const prompt = new FormData(formEl).get('prompt');
            const requestData = {
    prompt:"prompt"
};
            try {
                const response = await fetch(
                    'http://localhost:5000/chain', {
                        signal: aborter.signal,
                        method: 'POST',
                        headers: {'Content-Type': 'application/json',
                        body: JSON.stringify({}),
                    }
                });
                console.log(222);
                const reader = response.body.getReader();
                const decoder = new TextDecoder();
                while (true) {
                    const { done, value } = await reader.read();
                    if (done) { break; }
                    const decoded = decoder.decode(value, {stream: true});
                    console.log(decoded);
                    outputEl.innerText += decoded;
                }
            } catch (err) {
                console.error(err);
            }
        }
        run();  // run on initial prompt
        formEl.addEventListener('submit', function(event) {
            event.preventDefault();
            run();
        });
    </script>
</body>
</html>
''', mimetype='text/html')


def print_answer():
    global answer
    while True:
        if answer != "":
            print("总体答案:", answer)
            answer = ""  # 清空答案
        # 可以添加适当的延时，避免过于频繁地检查答案


if __name__ == '__main__':
    threading.Thread(target=print_answer).start()  # 启动打印答案的线程
    app.run(threaded=True, debug=True, port=5000, host='0.0.0.0')

import queue
import threading

from dotenv import load_dotenv
from flask import Flask, request, Response
from flask_cors import CORS
from langchain.chains import ConversationalRetrievalChain
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.output_parsers import StrOutputParser

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


def llm_thread(g, cat,question, chat_history):
    try:
        llm = ChatTongyi(
            callbacks=[ChainStreamHandler(g)],
            model="qwen-max",
            streaming=True
        )
        chain = ConversationalRetrievalChain.from_llm(
            llm,
            chain_type="stuff",
            retriever=get_retrieval(cat),
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


@app.route('/chain', methods=['POST'])
def _chain():
    question = '重庆有哪些好玩的地方,100字以上'
    return Response(chain(question, []), mimetype='text/event-stream')


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
            try {
                const response = await fetch(
                    'http://192.168.223.26:5000/chain', {
                        signal: aborter.signal,
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({
                            prompt
                        }),
                    }
                );
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


if __name__ == '__main__':
    app.run(threaded=True, debug=True, port=5000, host='0.0.0.0')

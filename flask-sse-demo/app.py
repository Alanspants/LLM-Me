import itertools
import time

from flask import Flask, render_template, Response

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.post("/start-connection")
def start_connection():
    return """<div hx-ext="sse" sse-connect="/connect" sse-swap="message">
        Contents of this box will be updated in real time
        with every SSE message received from the chatroom.
    </div>"""

@app.route("/connect")
def publish_hello():
    def stream():
        for idx in itertools.count():
            msg = f"data: <p>This is {idx}.</p>\n\n"
            yield msg
            time.sleep(1)

    return Response(stream(), mimetype="text/event-stream")

@app.post("/ping")
def route_clicked():
    return """<button hx-post="/pong" hx-swap="outerHTML">Pong</button>"""

@app.post("/pong")
def route_pong():
    return """<button hx-post="/ping" hx-swap="outerHTML">Ping</button>"""

if __name__ == "__main__":
    app.run(port=5050,debug=True)
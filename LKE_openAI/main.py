from flask import Flask, request, render_template, session, redirect, jsonify

app = Flask(__name__)


@app.route("/index")
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(port=5000)

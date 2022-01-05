from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return "Welcome to index page"


@app.route("/hi/")
def who():
    return "who are you"


@app.route("/hi/<username>")
def greet(username):
    return f"Hi there {username}"


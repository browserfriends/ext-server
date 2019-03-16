from flask import Flask, render_template
import sqlite3

application = Flask(__name__)


@application.route("/")
def home():
    return "Welcome to Browserfriends Server!"

@application.route("/api/down/<id>", methods=['GET'])
def fetch(id):
    return "down"

@application.route("/api/up/open", methods=['POST'])
def open():
    # add to db
    return "open!"

@application.route("/api/up/close", methods=['POST'])
    # add to db
    return "close!"

@application.route()
if __name__ == "__main__":
    application.run(debug=True)
    application.run(host='0.0.0.0')

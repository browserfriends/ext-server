from flask import Flask, render_template

application = Flask(__name__)


@application.route("/")
def home():
    return "Welcome to Browserfriends Server!"

if __name__ == "__main__":
    application.run(debug=True)
    application.run(host='0.0.0.0')

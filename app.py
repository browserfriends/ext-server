from flask import Flask, render_template, request

application = Flask(__name__)

# domain:list of ids
# id:curr_loc
id_domain = {}
id_loc = {}

@application.route("/")
def home():
    return "Welcome to Browserfriends Server!"

@application.route("/api/down/id", methods=['GET'])
def fetch():
    return "down"

@application.route("/api/up/open", methods=['POST'])
def open():
    # add new id/domain pair to the map
    if request.method == "POST":
        id = request.form['id']
        domain = request.form['url']
        if id in id_domain:
            # update
            print("yo wtf")
    else:
        return "Invalid open request"
    return "open!"

@application.route("/api/up/close", methods=['POST'])
    # add to db
def close():
    return "close!"

if __name__ == "__main__":
    application.run(debug=True)
    application.run(host='0.0.0.0')

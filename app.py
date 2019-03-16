from flask import Flask, render_template, request
import json

application = Flask(__name__)

# domain:list of ids
# id:curr_loc
id_domain = {} #stores last domain user had open domain:open?
id_loc = {}

@application.route("/")
def home():
    return "Welcome to Browserfriends Server!"

@application.route("/api/down/id", methods=['GET'])
def fetch():
    # return json!
    return json.dumps({'id': "someid"})

@application.route("/api/up/loc", methods=['POST'])
def location():
    if request.method == "POST":
        req = request.json
        id = req['id']
        lat = req['lat']
        long = req['long']
        id_loc[id] = loc
    else:
        return "Invalid loc request"
    return "loc!"

@application.route("/api/up/open", methods=['POST'])
def open():
    # add new id/domain pair to the map
    if request.method == "POST":
        print(request.form)
        id = request.form['id']
        domain = request.form['url']
        id_domain[id] = "{}.{}".format(domain, "open")
    else:
        return "Invalid open request"
    return "open!"

@application.route("/api/up/close", methods=['POST'])
def close():
    if request.method == "POST":
        id = request.form['id']
        domain = request.form['url']
        id_domain[id] = "{}.{}".format(domain, "closed")
    else:
        return "Invalid open request"
    return "close!"

@application.route("/view-stats")
def view():
    return render_template("debug.html", id_domain=id_domain, id_loc=id_loc)

if __name__ == "__main__":
    application.run(debug=True)
    application.run(host='0.0.0.0')

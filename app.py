from flask import Flask, render_template, request
import json

application = Flask(__name__)

# domain:list of ids
# id:curr_loc
id_domain = {} #stores last domain user had open domain:open?
id_loc = {}
# domain mapped to list of ids that are there
domain_id = {}

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
        print(req)
        id = req['id']
        lat = req['lat']
        lon = req['lon']
        id_loc[id] = (lat, lon)
    else:
        return "Invalid loc request"
    return "loc!"

@application.route("/api/up/open", methods=['POST'])
def open():
    # add new id/domain pair to the map
    if request.method == "POST":
        req = request.json
        print(req)
        id = req['id']
        domain = req['url']
        id_domain[id] = "{}.{}".format(domain, "open")
        if domain in domain_id:
            domain_id[domain].append(id)
        else:
            domain_id[domain] = [id]
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
    return render_template("debug.html", id_domain=id_domain, id_loc=id_loc, domain_id=domain_id)

if __name__ == "__main__":
    application.run(debug=True)
    application.run(host='0.0.0.0')

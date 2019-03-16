from flask import Flask, render_template, request
import json
import random
import time

application = Flask(__name__)

# domain:list of ids
# id:curr_loc
id_domain = {} #stores last domain user had open domain:open?
id_loc = {}
# domain mapped to list of ids that are there
domain_id = {}
# ids to last connection time
id_time = {}
curr_id = 0


def clean_clients():
    victims = [i for (i, t) in id_time.items() if t + 15 < time.time()]
    for v in victims:
        del id_time[v]
        if id in id_domain:
            del id_domain[v]

    for key, value in domain_id.items():
        domain_id[key] = [i for i in value if i not in victims]


def gen_id():
    global curr_id
    last_id = curr_id
    curr_id += 1
    return last_id

@application.route("/")
def home():
    return "Welcome to Browserfriends Server!"

@application.route("/api/down/id", methods=['GET'])
def fetch():
    # return json!
    new_id = gen_id()
    return json.dumps({'id': new_id})

@application.route("/api/down/control", methods=['GET'])
def command():
    # return json!
    id_time[request.args.get('id')] = time.time()
    clean_clients()
    if random.randint(0, 10) > 5:
        return json.dumps({'type': 'notify', 'title': 'This is the server.', 'content': "You are client " + request.args.get('id')})
    else:
        return json.dumps({'type': 'nop'})

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
        if not domain in domain_id:
            domain_id[domain] = []
        curr = domain_id[domain]
        curr.append(id)
        curr = set(curr)
        domain_id[domain] = curr
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
    clean_clients()
    return render_template("debug.html", id_domain=id_domain, id_loc=id_loc, domain_id=domain_id)

if __name__ == "__main__":
    application.run(debug=True)
    application.run(host='0.0.0.0')

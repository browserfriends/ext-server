from flask import Flask, render_template, request
import json
import random
import time
from geopy.distance import geodesic

from commands import sharedsite

commands = [
    sharedsite,
    youtube
]

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

def find5(src):
    print(id_loc)
    if src not in id_loc:
        print(src)
        return []
    id2loc = id_loc.items()     # list of tuples: (id, (lat, long))
    sorted(id2loc, key=lambda loc: geodesic(id_loc[src], loc[1]).meters)
    ret = [(i, geodesic(id_loc[src], d).meters) for i, d in id2loc if geodesic(id_loc[src], d).meters < 1000 and not i == src]
    if len(id2loc) < 5:
        return ret
    else:
        return ret[:5]

def clean_clients():
    victims = [i for (i, t) in id_time.items() if t + 15 < time.time()]
    for v in victims:
        del id_time[v]
        if v in id_domain:
            del id_domain[v]
        if v in id_loc:
            del id_loc[v]

    # url -> ids
    for key, value in domain_id.items():
        domain_id[key] = [i for i in value if i not in victims]


def gen_id():
    global curr_id
    last_id = curr_id
    curr_id += 1
    return str(last_id)

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
    if random.randint(0, 30) > 20:
        count = 0
        cmd = random.choice(commands)
        result = cmd.runcmd(request.args.get('id'), find5(request.args.get('id')), domain_id, id_domain)
        while result['type'] == 'nop' or count < 5:
            count += 1
            cmd = random.choice(commands)
            result = cmd.runcmd(request.args.get('id'), find5(request.args.get('id')), domain_id, id_domain)
        return json.dumps(result)
        # do a while loop, try to get it to not be nop
        # also extract actual url from id_domain dict

        # return json.dumps(cmd.runcmd(request.args.get('id'), find5(request.args.get('id')), domain_id, id_domain))
        # return json.dumps({'type': 'notify', 'title': 'This is the server.', 'content': "You are client " + request.args.get('id')})
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

@application.route("/api/friends") #this should be able to refer to the client's ID
def friends():
    if request.method == "GET":
        nearby_ids = find5(request.args.get('id'))
        dict = {
            'ids': nearby_ids,
            'acts': [(id_domain[i] if i in id_domain else "unknown") for (i, d) in nearby_ids]
        };
        return json.dumps(dict)
    else:
        return "Invalid friendship request"

@application.route("/api/up/open", methods=['POST'])
def open():
    # add new id/domain pair to the map
    if request.method == "POST":
        req = request.json
        print(req)
        id = req['id']
        domain = req['url']
        full = req['fullURL']
        id_domain[id] = "{}.{}".format(full, "open")
        if not domain in domain_id:
            domain_id[domain] = []
        curr = domain_id[domain]
        curr.append(id)
        curr = list(set(curr))
        domain_id[domain] = curr
        return "Invalid open request"
    return "open!"

@application.route("/api/up/close", methods=['POST'])
def close():
    if request.method == "POST":
        req = request.json
        id = req['id']
        domain = req['url']
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

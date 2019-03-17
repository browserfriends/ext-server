import random

def dictToList(dict):
    l = []
    for (domain, ids) in dict.items():
        l.append((domain, ids))
    return l


def runcmd(id, closest, domain_id, id_domain):
    if len(domain_id) > 0:
        print(domain_id)
        li = dictToList(domain_id)
        random.shuffle(li)

        for (domain, ids) in li:
            if id in ids:
                close = [i for i in ids if i in [i[0] for i in closest]]
                print(close)
                if len(close) > 0:
                    return {'type': 'notify', 'title': 'Shared site!', 'content': "Someone near you is also using " + domain + ", you should go find them!"}
    return {'type': 'nop'}

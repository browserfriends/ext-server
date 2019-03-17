import random

def dictToList(dict):
    l = []
    for (domain, ids) in dict.items():
        l.append((domain, ids))
    return l

def runcmd(id, closest, domain_id, id_domain):
    id2domain = dictToList(id_domain)
    random.shuffle(id2domain)

    for id, domain in id2domain:
        if "youtube" in domain:
            if id in closest:
                return {'type': 'link', 'title': 'Cool video!', \
                    'content': 'Someone near you is watching a video at ' + domain + ', check it out!'}
    return {'type': 'nop'}
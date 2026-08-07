import json, os, urllib.request
cfg = json.load(open(os.path.expanduser('~/clout/config.json')))
url = f"{cfg['relay']['server']}/{cfg['relay']['asks_topic']}/json?poll=1&since=all"
for line in urllib.request.urlopen(url).read().decode().splitlines():
    try: m = json.loads(line)
    except: continue
    if m.get("event") != "message": continue
    try: ask = json.loads(m["message"])
    except Exception as e: print("parse fail:", e); continue
    aid = ask.get("id","unknown")
    p = os.path.expanduser(f"~/clout/inbox/{aid}.json")
    r = os.path.expanduser(f"~/clout/outbox/{aid}-response.json")
    if not os.path.exists(p) and not os.path.exists(r):
        json.dump(ask, open(p,"w"), indent=1); print(f"new ask -> inbox/{aid}.json")
    else: print(f"already have {aid}")

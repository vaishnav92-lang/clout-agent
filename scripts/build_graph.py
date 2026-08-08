#!/usr/bin/env python3
"""Build ~/clout/graph/nodes.csv from whatever exists — never blocks on a download.
Order: LinkedIn Connections.csv (dropbox, else ~/Downloads) as the spine if present,
then iMessage warmth overlay, then any Gmail warmth already noted. If no LinkedIn
export is found, builds an iMessage-only warm graph so matching can start NOW."""
import csv, sqlite3, glob, re, os, sys

HOME = os.path.expanduser("~")
def norm(n): return re.sub(r'[^a-z ]','', (n or '').lower()).strip()
nodes = {}

# --- LinkedIn spine: find Connections.csv anywhere plausible ---
cands = (glob.glob(f"{HOME}/clout/dropbox/**/Connections.csv", recursive=True)
         + glob.glob(f"{HOME}/Downloads/**/Connections.csv", recursive=True))
li = 0
if cands:
    conn = cands[0]
    lines = open(conn, errors="ignore").read().split("\n")
    try:
        hi = next(i for i,l in enumerate(lines) if l.startswith("First Name,"))
        for r in csv.DictReader(lines[hi:]):
            if not (r.get("First Name") or "").strip(): continue
            nm = f"{r['First Name'].strip()} {r.get('Last Name','').strip()}"
            nodes[norm(nm)] = {"name":nm,"company":r.get("Company",""),"position":r.get("Position",""),
                "linkedin":r.get("URL",""),"email":r.get("Email Address",""),"warmth":0,
                "evidence":[],"last_alive":r.get("Connected On",""),"sources":"linkedin"}
        li = len(nodes)
    except StopIteration: pass

# --- iMessage warmth ---
num2name = {}
for db in glob.glob(f"{HOME}/Library/Application Support/AddressBook/**/AddressBook-v22.abcddb", recursive=True):
    try:
        c = sqlite3.connect(db)
        for full,num in c.execute("SELECT r.ZFIRSTNAME||' '||COALESCE(r.ZLASTNAME,''),p.ZFULLNUMBER FROM ZABCDPHONENUMBER p JOIN ZABCDRECORD r ON p.ZOWNER=r.Z_PK WHERE r.ZFIRSTNAME IS NOT NULL"):
            d = re.sub(r'\D','',num or '')[-10:]
            if d: num2name[d] = full.strip()
        c.close()
    except Exception: pass
imadd = 0
try:
    im = sqlite3.connect(f"{HOME}/Library/Messages/chat.db")
    q = """WITH dm AS(SELECT chat_id,MIN(handle_id) hid FROM chat_handle_join GROUP BY chat_id HAVING COUNT(DISTINCT handle_id)=1),
    m AS(SELECT d.hid,mm.is_from_me,mm.date FROM chat_message_join cj JOIN dm d ON cj.chat_id=d.chat_id JOIN message mm ON mm.ROWID=cj.message_id WHERE mm.date/1000000000+978307200>strftime('%s','now')-730*86400)
    SELECT h.id,COUNT(*),SUM(is_from_me),date(MAX(m.date)/1000000000+978307200,'unixepoch'),COUNT(DISTINCT strftime('%Y-%m',m.date/1000000000+978307200,'unixepoch')) FROM m JOIN handle h ON h.ROWID=m.hid GROUP BY h.id HAVING COUNT(*)>=30 AND SUM(is_from_me)>=8"""
    for hid,total,sent,last,months in im.execute(q):
        if "@" in hid: continue
        nm = num2name.get(re.sub(r'\D','',hid)[-10:])
        if not nm: continue
        k = norm(nm); w = 3 if (months>=12 and total>=300) else 2
        ev = f"imessage:{total}msgs/{months}mo,last {last}"
        if k in nodes:
            nodes[k]["warmth"]=max(nodes[k]["warmth"],w); nodes[k]["evidence"].append(ev)
            nodes[k]["sources"]+="+imsg"; nodes[k]["last_alive"]=max(nodes[k]["last_alive"] or "",last)
        else:
            nodes[k]={"name":nm,"company":"","position":"","linkedin":"","email":"","warmth":w,
                "evidence":[ev],"last_alive":last,"sources":"imessage"}; imadd+=1
except Exception as e:
    print(f"(iMessage skipped: {e})", file=sys.stderr)

os.makedirs(f"{HOME}/clout/graph", exist_ok=True)
with open(f"{HOME}/clout/graph/nodes.csv","w",newline="") as f:
    w = csv.writer(f); w.writerow(["name","warmth","warmth_evidence","company","position","linkedin","email","last_alive","sources"])
    for n in sorted(nodes.values(), key=lambda x:(-x["warmth"], x["name"])):
        w.writerow([n["name"],n["warmth"],"; ".join(n["evidence"]),n["company"],n["position"],n["linkedin"],n["email"],n["last_alive"],n["sources"]])
warm = sum(1 for n in nodes.values() if n["warmth"]>=2)
src = "LinkedIn+iMessage" if li else "iMessage-only (no LinkedIn export found yet)"
print(f"graph built: {len(nodes)} nodes ({src}), {warm} warm -> ~/clout/graph/nodes.csv")

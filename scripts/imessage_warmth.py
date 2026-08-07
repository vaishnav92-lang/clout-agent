#!/usr/bin/env python3
"""iMessage warmth extractor — runs entirely locally.
Reads chat.db (requires Full Disk Access for the hosting terminal app) and the
AddressBook, computes two-way warmth per 1:1 contact, prints ranked stats.
NO message content is printed by default — metadata only. Content sampling for
professional classification is a separate, explicit flag (--sample), and even
then samples stay on this machine (the agent reads them; they are never stored).
"""
import sqlite3, glob, re, sys, json, os

MONTHS = 24
MIN_TOTAL, MIN_EACH_WAY = 30, 8
sample = '--sample' in sys.argv
topn = int(sys.argv[sys.argv.index('--top')+1]) if '--top' in sys.argv else 40

num2name = {}
for db in glob.glob(os.path.expanduser('~/Library/Application Support/AddressBook/**/AddressBook-v22.abcddb', recursive=True):
    try:
        c = sqlite3.connect(db)
        for full, num in c.execute("SELECT r.ZFIRSTNAME||' '||COALESCE(r.ZLASTNAME,''), p.ZFULLNUMBER FROM ZABCDPHONENUMBER p JOIN ZABCDRECORD r ON p.ZOWNER=r.Z_PK WHERE r.ZFIRSTNAME IS NOT NULL"):
            d = re.sub(r'\D','', num or '')[-10:]
            if d: num2name[d] = full.strip()
        c.close()
    except Exception: pass

im = sqlite3.connect(os.path.expanduser('~/Library/Messages/chat.db'))
q = f"""WITH dm AS (SELECT chat_id, MIN(handle_id) hid FROM chat_handle_join GROUP BY chat_id HAVING COUNT(DISTINCT handle_id)=1),
m AS (SELECT d.hid,mm.is_from_me,mm.date FROM chat_message_join cj JOIN dm d ON cj.chat_id=d.chat_id JOIN message mm ON mm.ROWID=cj.message_id
WHERE mm.date/1000000000+978307200 > strftime('%s','now')-{MONTHS*30}*86400)
SELECT h.id, COUNT(*), SUM(is_from_me), date(MAX(m.date)/1000000000+978307200,'unixepoch'),
COUNT(DISTINCT strftime('%Y-%m', m.date/1000000000+978307200,'unixepoch'))
FROM m JOIN handle h ON h.ROWID=m.hid GROUP BY h.id
HAVING COUNT(*)>={MIN_TOTAL} AND SUM(is_from_me)>={MIN_EACH_WAY} AND COUNT(*)-SUM(is_from_me)>={MIN_EACH_WAY}
ORDER BY COUNT(DISTINCT strftime('%Y-%m', m.date/1000000000+978307200,'unixepoch')) DESC, COUNT(*) DESC"""

out = []
for hid,total,sent,last,months in im.execute(q):
    name = num2name.get(re.sub(r'\D','',hid)[-10:]) if '@' not in hid else hid
    rec = {"contact": name or hid, "handle": hid, "msgs": total, "sent": sent,
           "received": total-sent, "months_active": months, "last": last}
    if sample:
        rows = im.execute("""SELECT mm.text FROM message mm JOIN handle h ON mm.handle_id=h.ROWID
            WHERE h.id=? AND mm.text IS NOT NULL AND length(mm.text)>20 ORDER BY mm.date DESC LIMIT 3""",(hid,)).fetchall()
        rec["_samples"] = [ (r[0] or '').replace('\n',' ')[:80] for r in rows ]
    out.append(rec)
    if len(out) >= topn: break
print(json.dumps(out, indent=1, ensure_ascii=False))

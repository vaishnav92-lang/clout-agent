---
name: clout-inbox
description: "The auditable sharing gate: check ~/clout/inbox/ for asks from the Clout network agent, and for each one render the full disclosure card — the question verbatim, what your agent found in your PRIVATE graph, and the EXACT payload proposed to be sent back — then let the user approve, trim, refer someone, or decline. Nothing ever leaves without an explicit click. Invoke when the user says 'check my clout inbox', 'any asks for me', or a notification says an ask arrived."
---

# /clout-inbox — see every question, approve every answer

## 1. Read pending asks
Asks are JSON files in `~/clout/inbox/` not yet answered (no matching file in
`~/clout/outbox/`). Schema: {id, from, created, ask_type, role_title,
structured_ask{domain, capabilities, constraints, archetypes}, response_options}.

## 2. Match locally — private, full detail
For each ask, search `~/clout/graph/nodes.csv` (and only it — this skill never
touches mail/messages) using the ask's archetypes/signatures: candidates AND
people-who-might-know. Full findings stay in the private block.

## 3. Render THE CARD — a labeled dialogue between two parties
```
══ CLOUT AGENT SAYS ═══════════════════════════════════════
"We have one open job: <role_title>.
 <question_verbatim>
 May your agent search your network graph for matches?
 We will only ever receive what you explicitly approve."

── YOUR AGENT (runs on this machine, works only for you) ──
Clout is asking me to search your local graph (graph/nodes.csv
only — never your mail or messages). Run the search?
```
**Gate 1 — run the search?** Options: Search my graph / Refuse the ask
(sends "declined", nothing searched). Only on approval, search, then:
```
── YOUR AGENT · what I found (PRIVATE — Clout cannot see this) ──
• <name> — <why> · warmth <n> (<evidence>)
• ...

══ CLOUT AGENT RECOMMENDS ═════════════════════════════════
"Ideally: names + one-line context so we can pursue. But the
 default is counts only — your call entirely."

── YOUR AGENT · proposed payload (the EXACT bytes to send) ──
"<payload>"
→ contains: <inventory — e.g. match count only; no names, no contact info>
```
**Gate 2 — what goes back?** Options (most-trimmed first): Send counts only /
Send names + context / Offer to refer someone (double opt-in + their own email) /
Edit the payload / Decline.
On send: echo "SENT TO CLOUT: <payload>" so the release moment is explicit.

## 4. Release + ledger
Write the chosen payload to `~/clout/outbox/<id>-response.json`. Append to
`~/clout/ledger/ledger.md`:
```
## [timestamp] ask <id> from <from>
- question: <one line>
- found privately: N candidates, M connectors (names NOT logged here if declined)
- sent: "<exact payload>"
- withheld: <what the user chose not to share>
```

## Boundaries
- This skill reads ONLY graph/nodes.csv and inbox/. Never mail, messages, files.
- Nothing is written to outbox/ without a widget selection this session.
- Contact fields never cross: schema-enforced, not judgment-enforced.

## Watch mode — the server initiates, you only consent
When the user says "wait for asks" / "watch my clout inbox": run a foreground
poll loop (`until` new file appears: `python3 ~/clout/scripts/relay_pull.py`
every ~15s, announce "watching — asks will appear here the moment they arrive").
When an ask lands, IMMEDIATELY render its card and proceed through the gate.
Real-life equivalent (set up by /clout-setup): a launchd job auto-pulls at
boot/daily, and the member's phone subscribes to their ntfy asks topic — the
push notification IS the doorbell; the terminal is only needed to answer it.

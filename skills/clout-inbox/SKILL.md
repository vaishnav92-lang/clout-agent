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

## 3. Render THE CARD — exactly this shape
```
── Incoming ask #<id> · from <from> · <created> ─────────────
THE QUESTION (verbatim):
"<structured_ask rendered as the asker wrote it>"

WHAT YOUR AGENT FOUND (private — only you see this):
• <name> — <why they match> · warmth <n> (<evidence>)
• ...

PROPOSED RESPONSE (the exact payload that would be sent):
"<payload text>"
→ contains: <inventory: e.g. 'match count only. No names, no orgs,
   no contact info'>
```
The payload schema HAS NO FIELDS for phone/email — contact info is structurally
impossible to send. Default proposal = counts only (most-trimmed).

## 4. The gate (selection widget)
Options, always in this order (most-trimmed first):
1. **Send as proposed** (counts only)
2. **Send with names + one-line context**
3. **Offer to refer someone** — user picks who; the flow notes that the person
   will be pinged for consent + their preferred email BEFORE any referral is
   released (double opt-in; their reply is the only source of contact info)
4. **Edit what goes back** — user's text becomes the payload verbatim
5. **Decline** — sends "no matches"

## 5. Release + ledger
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

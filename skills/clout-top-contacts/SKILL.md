---
name: clout-top-contacts
description: "The Clout warm-network discovery moment: with the user's explicit approval, scan their iMessage history LOCALLY (metadata first, content sampling only under a second approval), identify their top professional contacts, and recommend which to add to their Clout graph — each addition individually approved. Invoke when the user says 'find my top contacts', 'who are my warmest professional contacts', or during onboarding after /clout-setup."
---

# /clout-top-contacts — your warmest professional relationships, from your own texts

Everything runs on this machine. Nothing is transmitted anywhere. The output is a
recommendation list the user approves person-by-person into their local graph.

## 1. The capability card — BEFORE touching anything

Render this and get explicit approval via the selection widget:

```
── Capability request ─────────────────────────────
Your agent wants to: scan your iMessage history (local database)
It will read:  per-contact message COUNTS, dates, and direction
               (who you text, how often, how recently)
It will NOT:   read message content in this pass, store any message
               text, or transmit anything off this machine
Requires:      Full Disk Access for your terminal app (macOS setting)
```
Options: **Approve metadata scan** / Decline.
If FDA isn't granted yet, walk them through System Settings → Privacy & Security
→ Full Disk Access → add their terminal app → restart it, then resume.

## 2. Metadata scan

Run `python3 ~/clout/scripts/imessage_warmth.py --top 40` (note: needs
dangerouslyDisableSandbox-equivalent / unsandboxed shell for chat.db).
This yields ranked two-way warmth stats: contact name (via local AddressBook),
message counts both directions, months active, last contact. Show the top of it.

## 3. Second capability card — content sampling for classification

To separate professional from personal, the agent needs to glance at 2-3 recent
snippets per top contact. Second card:
```
Your agent wants to: read 2-3 short recent snippets per top-40 contact,
once, to classify professional vs personal. Snippets are read and
discarded — never stored, never transmitted.
```
Options: **Approve sampling** / Skip (classification falls back to the user
tagging contacts themselves — offer the list with tag-it-yourself).

## 4. Classify and present the top professional contacts

Run with `--sample`, read the snippets, classify each contact: professional /
semi / personal, with a one-line evidence note ("refers candidates by email",
"comp calibration talk"). NEVER echo raw message text into the final output —
paraphrase the evidence. Present the top 5 professional contacts with warmth
stats and the evidence line.

## 5. Recommend additions to the graph — each one approved

For each of the top 5 (and any near-misses worth offering):
"Add to your Clout graph?" — per-person approve/skip via the widget.
Approved ones are appended to `~/clout/graph/nodes.csv` with warmth score,
evidence summary, and source=imessage. Skipped ones are NOT recorded anywhere.

## 6. Ledger

Append to `~/clout/ledger/ledger.md`:
```
## [timestamp] clout-top-contacts run
- capability: imessage metadata scan — APPROVED [time]
- capability: content sampling — APPROVED/DECLINED [time]
- read: N contacts' metadata; sampled M contacts
- stored: K contacts added to graph (names); 0 message content stored
- transmitted: nothing
```
The ledger is the user's audit trail — every run appends, nothing is deleted.

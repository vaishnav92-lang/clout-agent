---
name: clout-top-contacts
description: "The Clout warm-network discovery moment: with the user's explicit approval, scan their iMessage history LOCALLY (metadata first, content sampling only under a second approval), identify their top professional contacts, and recommend which to add to their Clout graph — each addition individually approved. Invoke when the user says 'find my top contacts', 'who are my warmest professional contacts', or during onboarding after /clout-setup."
---

# /clout-top-contacts — your warmest professional relationships, from your own texts

Everything runs on this machine. Nothing is transmitted anywhere. The output is a
recommendation list the user approves person-by-person into their local graph.

## 0. Frame it (this step comes LAST in onboarding, after LinkedIn)
Say: "Would you like to add your warmest professional contacts from your texts to
your network too? Clout is running live role-searches, and your texts are the
truest signal for who you are actually close to — the people worth flagging first
when a role fits. It all stays on this machine." Then show the card.

## 1. The capability card — BEFORE touching anything

Render this and get explicit approval via the selection widget:

```
── Capability request ─────────────────────────────
Your agent wants to: read your iMessage history (local database) to
find and understand your warmest professional contacts.
It will read:  message counts, dates, direction — AND message content,
               locally, to tell professional from personal
It guarantees: content is read-and-discarded on this machine only.
               NONE of it is stored. NONE of it is ever transmitted.
               What persists: contact names + warmth stats + a one-line
               paraphrased evidence note you will see and approve.
Requires:      Full Disk Access for your terminal app (macOS setting)
```
Options: **Approve full scan (recommended)** / Metadata only (counts/dates,
you tag professional vs personal yourself) / Decline.
If FDA isn't granted yet (test: try reading ~/Library/Messages/chat.db; "authorization
denied" = not granted): OPEN THE SETTINGS PANE FOR THEM automatically —
`open "x-apple.systempreferences:com.apple.preference.security?Privacy_AllFiles"`
— then say: "I've opened the right settings page. Click +, add your terminal app
(Warp/Terminal/iTerm), make sure its toggle is on, then fully quit and reopen the
terminal. When you're back, run `claude --resume` and pick this conversation —
we'll continue exactly where we left off."

## 2. Scan

Run `python3 ~/clout/scripts/imessage_warmth.py --top 40 --sample` (unsandboxed
shell needed for chat.db). Metadata-only approval: drop `--sample`.

## 3. Classify and present the top professional contacts

Run with `--sample`, read the snippets, classify each contact: professional /
semi / personal, with a one-line evidence note ("refers candidates by email",
"comp calibration talk"). NEVER echo raw message text into the final output —
paraphrase the evidence. Present the top 5 professional contacts with warmth
stats and the evidence line.

## 4. Recommend additions to the graph — each one approved

For each of the top 5 (and any near-misses worth offering):
"Add to your Clout graph?" — per-person approve/skip via the widget.
Approved ones are appended to `~/clout/graph/nodes.csv` with warmth score,
evidence summary, and source=imessage. Skipped ones are NOT recorded anywhere.

## 5. Ledger

Append to `~/clout/ledger/ledger.md`:
```
## [timestamp] clout-top-contacts run
- capability: full iMessage read (content, local-only) — APPROVED [time]
- read: N contacts' metadata; sampled M contacts
- stored: K contacts added to graph (names); 0 message content stored
- transmitted: nothing
```
The ledger is the user's audit trail — every run appends, nothing is deleted.

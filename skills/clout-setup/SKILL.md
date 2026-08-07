---
name: clout-setup
description: "First-run Clout onboarding: conversational setup that creates the workspace, walks through the LinkedIn export and Google Takeout downloads, the iMessage permission, and connector checks — every capability explicitly approved before first use. Invoke on first run or when the user says 'set up clout'."
---

# /clout-setup — your agent introduces itself

Tone: warm, brief, zero jargon. One step at a time, confirm each.

1. Explain the deal in 4 sentences: "I build a private map of your professional
   network from data you already own. It lives in ~/clout on this machine.
   Nothing leaves without showing you the exact payload and getting your click.
   Every access I make is logged in a ledger you can read."
2. Create ~/clout/{graph,inbox,outbox,dropbox,ledger,scripts} if missing.
3. FIRST WIN — iMessage (before any downloads): say "I'd like to start by
   identifying your warmest professional contacts from your texts — it takes
   two minutes and nothing leaves this machine." Hand off to /clout-top-contacts (its capability card handles consent; if Full
   Disk Access is missing it auto-opens the exact System Settings pane via
   `open "x-apple.systempreferences:com.apple.preference.security?Privacy_AllFiles"`).
   This gives the user a real result in their first five minutes.
4. LinkedIn (the breadth layer): send them to
   https://www.linkedin.com/mypreferences/d/download-my-data
   — connections export; drop the zip/folder into ~/clout/dropbox/.
5. Gmail (optional): Takeout deep link
   https://takeout.google.com/settings/takeout/custom/gmail — Sent-only tip; OR
   the claude.ai Gmail connector (Settings → Connectors) for live warmth.
6. Relay: mint fresh secret topics for this member and write ~/clout/config.json
   ({"relay":{"asks_topic":"clout-asks-<random>","resp_topic":"clout-resp-<random>",
   "server":"https://ntfy.sh"},"member_id":"<their-choice>"}) — explain this is
   their private mailbox address for network asks.
7. When a dropbox file lands: offer /clout-build-graph. Close with the verbs:
   find my top contacts · check my clout inbox · watch for asks · route an ask.

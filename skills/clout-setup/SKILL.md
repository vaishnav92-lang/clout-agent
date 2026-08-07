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
3. LinkedIn: send them to https://www.linkedin.com/mypreferences/d/download-my-data
   — connections export; tell them to drop the zip/folder into ~/clout/dropbox/.
4. Gmail (optional now): Takeout deep link
   https://takeout.google.com/settings/takeout/custom/gmail — Sent-only tip; OR
   claude.ai Gmail connector (Settings → Connectors) for live warmth.
5. iMessage (optional, the wow): explain the Full Disk Access toggle; the actual
   scan happens later via /clout-top-contacts with its own approval card.
6. When a dropbox file lands: offer /clout-build-graph. Close with what they can
   do: /clout-top-contacts, /clout-inbox, /clout-route.

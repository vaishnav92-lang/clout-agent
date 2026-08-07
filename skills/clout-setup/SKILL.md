---
name: clout-setup
description: "First-run Clout onboarding: lead with the live role-searches, then build the network graph — LinkedIn first, Gmail optional, warm iMessage contacts LAST as enrichment. Every capability explicitly approved before first use. Invoke on first run or when the user says 'set up clout'."
---

# /clout-setup — your agent introduces itself

Tone: warm, brief, zero jargon. One step at a time, confirm each.

1. LEAD WITH THE ROLES. Read ~/clout/live-roles.md and name 1-2 concrete current
   searches: "Clout is currently recruiting for roles like <A> and <B>. Members
   help by flagging who in their network could fit — or who might know good
   candidates. I do that by privately mapping your network on this machine; you
   approve every share and earn referral credit when your pick gets hired."
2. Create ~/clout/{graph,inbox,outbox,dropbox,ledger,scripts} if missing.
3. LINKEDIN FIRST — the breadth of the network. Send them to
   https://www.linkedin.com/mypreferences/d/download-my-data (connections export),
   have them drop the zip/folder into ~/clout/dropbox/, then run /clout-build-graph.
4. GMAIL (optional) — adds warmth: Takeout deep link
   https://takeout.google.com/settings/takeout/custom/gmail (Sent-only tip), OR the
   claude.ai Gmail connector (Settings → Connectors) for live warmth.
5. WARM CONTACTS LAST (enrichment): "Would you like to add your warmest
   professional contacts from your texts too? It's the truest signal for who you're
   actually close to, and it all stays on this machine." → hand to
   /clout-top-contacts (its card handles consent; if Full Disk Access is missing it
   auto-opens the exact pane via
   `open "x-apple.systempreferences:com.apple.preference.security?Privacy_AllFiles"`).
6. RELAY — mint fresh secret topics for this member and write ~/clout/config.json:
   {"relay":{"asks_topic":"clout-asks-<random>","resp_topic":"clout-resp-<random>",
   "server":"https://ntfy.sh"},"member_id":"<their-choice>"} — this is their private
   mailbox address for role-asks.
7. Close with the verbs: check my clout inbox · watch for asks · find my top
   contacts · route a role of my own.

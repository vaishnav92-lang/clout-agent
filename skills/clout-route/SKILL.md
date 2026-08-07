---
name: clout-route
description: "The Clout routing engine: given an ask — a JD, an intro request, a 'who do you know who…' — search the user's local network graph and return the top warm paths, each with who/why/warmth evidence and a drafted intro note. Invoke with the ask as args (/clout-route <paste JD or ask>), or when Vaishnav says 'route this', 'who in my network', 'find me paths to X'. Read-only on the graph; drafts intros but sends nothing."
---

# /clout-route — ask in, warm paths out

Input: an ask, in any form — a full JD, one line ("who do I know that could hire FDEs for EA orgs?"), or a forwarded email. Output: the top 3–5 paths through the user's own network, with drafted next steps. Nothing is sent; nothing leaves the machine.

## 1. Parse the ask
Extract: what's being sought (person to hire / intro / advice / distribution), the domain and seniority, hard constraints (location, timezone, clearance), and who's asking (affects tone of drafted intros). If the ask is genuinely ambiguous, ask ONE clarifying question, not a survey.

## 2. Search the graph — layered, warmest-first
Primary: `/Users/vaish/clout/graph/nodes.csv` — the unified graph (columns: name, emails, phones, linkedin, current_role, org, tags, warmth (0–3), warmth_evidence, last_alive, source, notes). If it doesn't exist or looks thin, say so and point the user to /clout-build-graph — never guess at a network.

Match on TWO axes, and keep them separate in your head:
- **Candidates** — people who could BE the thing sought.
- **Connectors** — people who likely KNOW the thing sought (recruiters, community nodes, people at relevant orgs, prior clients). A great connector often beats a mediocre candidate match; always surface both lists.

## 3. Score
fit (does their role/history actually match) × warmth (0=cold, 1=known, 2=warm, 3=close — from warmth_evidence, never guessed) × freshness (when was the relationship last alive). A warm 80% match outranks a cold 95% match — the product is paths, not a directory. NDA guard: client-derived candidate data routes only per its provenance/consent tags — METR/client pipeline people are NOT network nodes unless independently consented (check `source` and `notes`).

## 4. Output (report-shaped)
**Paths** — ranked, 3–5, each:
**1. [Name]** — why them (one line) · warmth: [level + evidence, e.g. "texts monthly, last 7/09"] · path: direct / via [connector]
Draft: the 2–3 sentence outreach or intro note, in Vaishnav's voice, ready to send.

**Connectors worth asking** — 1–3 who'd know someone, each with a drafted one-line ask.
**Nobody?** Say so honestly, name the closest misses and why they miss, and suggest which cold pool or channel would fill the gap. Never pad a weak list.

## Boundaries
- Read-only on every source; drafts are text in chat, sends are his.
- Never invent warmth or relationships; every warmth claim carries its evidence.
- Candid/client-derived reads never appear in drafted outreach text.

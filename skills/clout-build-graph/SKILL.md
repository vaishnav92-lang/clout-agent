---
name: clout-build-graph
description: "Build or refresh the local network graph (~/clout/graph/nodes.csv) from whatever sources exist: LinkedIn connections export in ~/clout/dropbox/, iMessage warmth (if approved), Gmail warmth (connector or Takeout mbox), and ANY context files the user drops in dropbox/ (old CRMs, notes, bios). Layered: LinkedIn = identity spine; messages/mail = warmth; user files = context. Invoke when an export lands or the user says 'build/refresh my graph'."
---

# /clout-build-graph

1. Inventory ~/clout/dropbox/: LinkedIn export (Connections.csv), Takeout mbox,
   anything else (CSVs, notes — ask the user what each is if unclear).
2. Run ~/clout/scripts/build_graph.py for the mechanical merge (LinkedIn spine +
   warmth layers). iMessage layer only if previously approved (check ledger).
3. Fold user-provided context files in as context notes on matching nodes
   (name-matched; ambiguous matches asked, never guessed).
4. Report: node count, warm count, multi-source count, what's missing.
5. Ledger entry: sources read, counts, nothing transmitted.
Enrichment (thread-context + web) is a separate deeper pass — offer it for the
top-N warm nodes only.

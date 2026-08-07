#!/bin/sh
# Clout member-agent installer. Copies skills into ~/.claude/skills and creates ~/clout.
set -e
REPO="https://raw.githubusercontent.com/vaishnav92-lang/clout-agent/main"
mkdir -p ~/clout/graph ~/clout/inbox ~/clout/outbox ~/clout/dropbox ~/clout/ledger ~/clout/scripts
for s in clout-setup clout-top-contacts clout-inbox clout-build-graph clout-route; do
  mkdir -p ~/.claude/skills/$s
  curl -fsSL "$REPO/skills/$s/SKILL.md" -o ~/.claude/skills/$s/SKILL.md
done
curl -fsSL "$REPO/workspace-CLAUDE.md" -o ~/clout/CLAUDE.md
curl -fsSL "$REPO/scripts/imessage_warmth.py" -o ~/clout/scripts/imessage_warmth.py
curl -fsSL "$REPO/scripts/build_graph.py" -o ~/clout/scripts/build_graph.py 2>/dev/null || true
echo ""
echo "Clout agent installed. Requirements: Claude Code + a Claude subscription."
echo "Start with:  cd ~/clout && claude \"set up clout\""


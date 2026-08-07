#!/bin/sh
# The ONLY code that touches the network.
#   pull            — fetch new asks from the relay into ~/clout/inbox/
#   push <file>     — print the exact payload, then POST it to the relay
set -e
CFG=~/clout/config.json
case "$1" in
  pull) python3 ~/clout/scripts/relay_pull.py ;;
  push)
    RESP=$(python3 -c "import json;print(json.load(open('$CFG'.replace('~',__import__('os').path.expanduser('~'))))['relay']['resp_topic'])" 2>/dev/null || python3 -c "import json,os;print(json.load(open(os.path.expanduser('$CFG')))['relay']['resp_topic'])")
    SERVER=$(python3 -c "import json,os;print(json.load(open(os.path.expanduser('$CFG')))['relay']['server'])")
    echo "--- payload leaving this machine (verbatim): ---"; cat "$2"; echo "--- end payload ---"
    curl -fsSL -X POST -d @"$2" "$SERVER/$RESP" >/dev/null && echo "sent."
    ;;
  *) echo "usage: relay_sync.sh pull | push <outbox-file>";;
esac

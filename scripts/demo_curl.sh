#!/usr/bin/env bash
set -euo pipefail

BRIDGE_URL="${BRIDGE_URL:-http://127.0.0.1:8787/run}"
TASK="${1:-Say hello from Hermes fake mode in one short sentence.}"
TOKEN="${HERMES_OPERATOR_TOKEN:-}"

args=(-sS -X POST "$BRIDGE_URL" -H "content-type: application/json")
if [[ -n "$TOKEN" ]]; then
  args+=(-H "Authorization: Bearer $TOKEN")
fi
args+=(-d "{\"task\":\"$TASK\"}")

curl "${args[@]}"
echo

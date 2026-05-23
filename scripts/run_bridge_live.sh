#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

HOST="${HERMES_OPERATOR_BRIDGE_HOST:-0.0.0.0}"
PORT="${HERMES_OPERATOR_BRIDGE_PORT:-8787}"

: "${HERMES_API_BASE_URL:=http://127.0.0.1:8642/v1}"
: "${HERMES_API_KEY:=local}"
: "${HERMES_API_MODEL:=hermes-agent}"
: "${HERMES_OPERATOR_TOKEN:=dev-token}"

export HERMES_API_BASE_URL HERMES_API_KEY HERMES_API_MODEL HERMES_OPERATOR_TOKEN
export HERMES_OPERATOR_FAKE_MODE=false

echo "Starting OpenHome Hermes Operator bridge against live Hermes"
echo "  bridge: http://$HOST:$PORT"
echo "  hermes api: $HERMES_API_BASE_URL"
echo "  hermes model: $HERMES_API_MODEL"
echo "  token set: yes"

echo
python3 -m uvicorn hermes_operator.app:app --host "$HOST" --port "$PORT"

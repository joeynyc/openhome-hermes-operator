#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

HOST="${HERMES_OPERATOR_BRIDGE_HOST:-0.0.0.0}"
PORT="${HERMES_OPERATOR_BRIDGE_PORT:-8787}"

export HERMES_OPERATOR_FAKE_MODE="${HERMES_OPERATOR_FAKE_MODE:-true}"
export HERMES_OPERATOR_TOKEN="${HERMES_OPERATOR_TOKEN:-dev-token}"

echo "Starting OpenHome Hermes Operator bridge"
echo "  host: $HOST"
echo "  port: $PORT"
echo "  fake mode: $HERMES_OPERATOR_FAKE_MODE"
echo "  token set: yes"

echo
python3 -m uvicorn hermes_operator.app:app --host "$HOST" --port "$PORT"

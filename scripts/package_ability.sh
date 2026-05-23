#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

OUT="${1:-/tmp/hermes-operator-openhome-ability.zip}"
ABILITY_DIR="openhome_ability"
ABILITY_NAME="hermes-operator"

if [[ ! -d "$ABILITY_DIR/$ABILITY_NAME" ]]; then
  echo "missing ability directory: $ABILITY_DIR/$ABILITY_NAME" >&2
  exit 1
fi

rm -f "$OUT"
(
  cd "$ABILITY_DIR"
  zip -qr "$OUT" "$ABILITY_NAME"
)

python3 - <<PY
import sys, zipfile
path = "$OUT"
required = {"$ABILITY_NAME/main.py", "$ABILITY_NAME/README.md"}
with zipfile.ZipFile(path) as zf:
    names = set(zf.namelist())
missing = sorted(required - names)
if missing:
    print(f"zip missing required files: {missing}", file=sys.stderr)
    sys.exit(1)
print(path)
PY

# OpenHome Hermes Operator

OpenHome voice control for Hermes Agent.

This turns an OpenHome DevKit into a local-first voice operator for real home-lab work: checking model servers, reading logs, running benchmarks, managing services, triggering Hermes skills, and speaking back short status summaries.

OpenHome is the microphone and speaker. Hermes is the agent brain.

## Status

Ready until the physical OpenHome device is available.

Already built and tested:

- FastAPI bridge
- OpenHome custom ability folder
- fake mode for local demos
- optional bearer-token auth
- Hermes OpenAI-compatible API client
- voice-safe response cleanup
- local CLI simulator
- ability zip packaging
- pytest + GitHub Actions CI

Still needs the device/dashboard:

- upload the custom ability zip
- configure trigger phrases
- set the bridge URL/token
- test the real voice loop

## Architecture

```text
OpenHome Ability -> local FastAPI bridge -> Hermes API Server -> tools/models/actions -> spoken summary
```

The OpenHome ability stays small. It captures a voice task, confirms it, sends it to the bridge, speaks `spoken_summary`, then resumes normal OpenHome flow.

## Quick start

```bash
git clone https://github.com/joeynyc/openhome-hermes-operator.git
cd openhome-hermes-operator
python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
python -m pytest tests -v
```

## Run fake mode

Fake mode works without an OpenHome device and without a live Hermes server.

Terminal 1:

```bash
source .venv/bin/activate
export HERMES_OPERATOR_TOKEN=dev-token
./scripts/run_bridge_fake.sh
```

Terminal 2:

```bash
export HERMES_OPERATOR_TOKEN=dev-token
./scripts/demo_curl.sh "check my local model server"
python -m hermes_operator.cli "check my local model server"
```

Expected:

```text
Hermes fake mode is working. I received: check my local model server
```

## Run with live Hermes

Start Hermes API Server separately, then run:

```bash
source .venv/bin/activate
export HERMES_API_BASE_URL=http://127.0.0.1:8642/v1
export HERMES_API_KEY=dev-token
export HERMES_API_MODEL=hermes-agent
export HERMES_OPERATOR_TOKEN=dev-token
./scripts/run_bridge_live.sh
```

Call the bridge:

```bash
python -m hermes_operator.cli "Say hello in one short sentence."
```

## Package for OpenHome

```bash
./scripts/package_ability.sh
```

Output:

```text
/tmp/hermes-operator-openhome-ability.zip
```

Upload that zip in the OpenHome dashboard when the device/account is ready.

Suggested device config:

```bash
OPENHOME_HERMES_BRIDGE_URL=http://192.168.1.201:8787/run
OPENHOME_HERMES_BRIDGE_TOKEN=dev-token
OPENHOME_HERMES_TIMEOUT=240
```

## API

```text
POST /run
Authorization: Bearer <token>   # only required if HERMES_OPERATOR_TOKEN is set
```

Request:

```json
{"task":"check my local model server","session_id":"optional"}
```

Response:

```json
{"ok":true,"spoken_summary":"short voice-safe answer","raw_text":"full Hermes response","artifact_path":null}
```

## Validate before hardware

```bash
source .venv/bin/activate
pip install -e '.[dev]'
python -m pytest tests -v
python -m build
./scripts/package_ability.sh
```

If those pass, the next step requires the physical OpenHome device.

## Docs

- `docs/architecture.md`
- `docs/pre-device-wiring.md`
- `docs/openhome-application.md`
- `openhome_ability/hermes-operator/README.md`

# OpenHome Hermes Operator

Voice bridge between OpenHome Abilities and Hermes Agent.

Goal: make an OpenHome DevKit act as a local-first voice interface for Hermes Agent and open-source models. OpenHome is the ears and mouth; Hermes is the operator brain that can use tools, memory, skills, local model routing, terminal access, smart-home integrations, GitHub workflows, cron jobs, and web research.

Repository: https://github.com/joeynyc/openhome-hermes-operator

## Current status

Ready up to the point where physical OpenHome hardware is required.

Validated locally:

- FastAPI bridge request/response flow
- optional bearer-token auth
- fake mode for pre-device demos
- OpenAI-compatible Hermes API client parsing
- voice-safe text cleanup for TTS
- local CLI simulator
- shell script syntax
- Python package build
- OpenHome ability zip packaging
- GitHub Actions test matrix

Hardware-only remaining:

- upload custom ability in the OpenHome dashboard
- configure trigger phrases on the device/account
- verify the device can reach the LAN bridge URL
- run the Live Editor/device voice loop
- confirm spoken TTS output from the physical speaker

## Concept

MVP voice flow:

1. User triggers the OpenHome ability with a phrase like "Hermes operator" or "Jetson".
2. Ability asks what Hermes should do.
3. User speaks a task.
4. Ability confirms before sending work.
5. Ability sends the task to the local bridge.
6. Bridge forwards the task to Hermes Agent, or returns fake-mode output for demos.
7. Ability speaks a concise voice-safe summary.

Example target demo:

```text
Jetson, check my local model server, run a quick benchmark, and tell me if anything crashed.
```

## Project layout

```text
bridge/hermes_operator/                 FastAPI bridge package
openhome_ability/hermes-operator/       OpenHome custom ability folder
docs/architecture.md                    architecture and security model
docs/pre-device-wiring.md               local runbook before hardware arrives
docs/openhome-application.md            DevKit application/pitch text
scripts/demo_curl.sh                    curl smoke test for /run
scripts/run_bridge_fake.sh              start bridge in fake mode
scripts/run_bridge_live.sh              start bridge against live Hermes API Server
scripts/package_ability.sh              create uploadable OpenHome ability zip
tests/                                  pytest suite
```

## Install for local development

```bash
cd /home/zerocool/projects/openhome-hermes-operator
python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
```

## Run tests

```bash
source .venv/bin/activate
python -m pytest tests -v
```

## Build Python package

```bash
source .venv/bin/activate
python -m build
```

Build outputs go to `dist/` and are ignored by git.

## Run bridge in fake mode

Fake mode does not need a live Hermes API Server. It is the main pre-device/pre-Hermes smoke-test path.

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

Expected summary:

```text
Hermes fake mode is working. I received: check my local model server
```

## Run bridge against live Hermes

The bridge calls the Hermes API Server OpenAI-compatible endpoint at `/v1/chat/completions`.

Default live-mode bridge settings:

```bash
HERMES_API_BASE_URL=http://127.0.0.1:8642/v1
HERMES_API_KEY=local
HERMES_API_MODEL=hermes-agent
HERMES_OPERATOR_TOKEN=dev-token
```

Start the bridge:

```bash
source .venv/bin/activate
export HERMES_API_KEY=dev-token
export HERMES_OPERATOR_TOKEN=dev-token
./scripts/run_bridge_live.sh
```

Call it:

```bash
export HERMES_OPERATOR_TOKEN=dev-token
python -m hermes_operator.cli "Say hello in one short sentence."
```

## Manual curl

```bash
curl -X POST http://127.0.0.1:8787/run \
  -H 'content-type: application/json' \
  -H "Authorization: Bearer $HERMES_OPERATOR_TOKEN" \
  -d '{"task":"Say hello in one short sentence"}'
```

If `HERMES_OPERATOR_TOKEN` is unset on the bridge, the authorization header is not required.

## Package the OpenHome ability

```bash
./scripts/package_ability.sh
```

Default output:

```text
/tmp/hermes-operator-openhome-ability.zip
```

The zip contains only the `hermes-operator/` ability folder, which is what should be uploaded to the OpenHome dashboard when the device/account is available.

## OpenHome ability runtime config

Set these in the OpenHome runtime/dashboard if supported:

```bash
OPENHOME_HERMES_BRIDGE_URL=http://192.168.1.201:8787/run
OPENHOME_HERMES_BRIDGE_TOKEN=dev-token
OPENHOME_HERMES_TIMEOUT=240
```

Use the LAN-accessible bridge URL for the device. Keep the Hermes API Server itself bound privately to localhost when possible; expose only the small bridge to the LAN.

## Safety model

- Bridge auth is optional but recommended on LAN.
- The ability asks for confirmation before sending the spoken task.
- Dangerous operations should rely on Hermes approval/safety settings.
- The bridge strips markdown/code fences and trims long responses before TTS.
- Secrets are not committed; use environment variables or `.env` files outside git.

## Validation checklist before hardware

```bash
source .venv/bin/activate
pip install -e '.[dev]'
python -m pytest tests -v
python -m build
./scripts/package_ability.sh
```

Then run fake mode and exercise both clients:

```bash
./scripts/run_bridge_fake.sh
# in another terminal:
export HERMES_OPERATOR_TOKEN=dev-token
./scripts/demo_curl.sh "start the LAN game server and tell me the URL"
python -m hermes_operator.cli "start the LAN game server and tell me the URL"
```

When those pass, the project is blocked only on the physical OpenHome device/dashboard upload step.

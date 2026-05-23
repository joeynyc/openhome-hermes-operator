# OpenHome Hermes Operator

Turn an OpenHome DevKit into a local-first voice operator for Hermes Agent and open-source models.

OpenHome supplies the voice interface: microphone, speaker, wake/trigger flow, and the ability runtime. Hermes supplies the operator brain: tools, memory, skills, terminal access, GitHub workflows, smart-home control, local model routing, web research, cron jobs, and infrastructure automation.

This repo is intentionally not a generic chatbot. It is a voice control layer for real local work:

```text
"Jetson, check my local model server, run a quick benchmark, and tell me if anything crashed."
```

Repository:
https://github.com/joeynyc/openhome-hermes-operator

## Status

Pre-device build is complete.

Everything that can be tested before having the physical OpenHome device has been built and validated:

- FastAPI bridge
- OpenHome custom ability folder
- optional bearer-token auth
- fake mode for demos without a live Hermes server
- OpenAI-compatible Hermes API client
- voice-safe response cleanup for TTS
- local CLI simulator
- curl smoke-test script
- repeatable ability zip packaging
- Python package build
- pytest suite
- GitHub Actions matrix for Python 3.10, 3.11, and 3.12

The remaining work requires the OpenHome device/dashboard:

- upload the custom ability zip
- configure trigger phrases
- set the bridge URL/token in the OpenHome runtime
- verify the device can reach the bridge over LAN
- test the Live Editor/device voice loop
- confirm real speaker TTS output

## What this builds

```text
voice command
  -> OpenHome ability
  -> local FastAPI bridge
  -> Hermes Agent API Server
  -> tools / skills / local models / infrastructure actions
  -> short voice-safe summary
  -> OpenHome speaks the result
```

The OpenHome ability stays thin. It captures the spoken request, confirms it, sends it to the local bridge, speaks the result, and returns OpenHome to normal flow.

The bridge does the heavier local work: validation, auth, fake mode, Hermes API calls, and response shaping for voice.

## Example use cases

- check local model servers
- summarize Docker/service health
- run a quick benchmark
- inspect logs and report failures
- start or stop local lab services after confirmation
- create or update GitHub issues
- trigger Hermes skills or workflows
- control smart-home devices through Hermes integrations
- ask a local/open-source model to reason over the result

## Project layout

```text
bridge/hermes_operator/                 FastAPI bridge package
openhome_ability/hermes-operator/       OpenHome custom ability folder
docs/architecture.md                    architecture and security model
docs/pre-device-wiring.md               full local pre-device runbook
docs/openhome-application.md            OpenHome DevKit pitch/application text
scripts/demo_curl.sh                    curl smoke test for /run
scripts/run_bridge_fake.sh              start bridge in fake mode
scripts/run_bridge_live.sh              start bridge against live Hermes API Server
scripts/package_ability.sh              create uploadable OpenHome ability zip
tests/                                  pytest suite
```

## Quick start

```bash
git clone https://github.com/joeynyc/openhome-hermes-operator.git
cd openhome-hermes-operator
python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
```

Run the validation suite:

```bash
python -m pytest tests -v
python -m build
./scripts/package_ability.sh
```

The ability zip is written to:

```text
/tmp/hermes-operator-openhome-ability.zip
```

## Run without an OpenHome device

Fake mode lets you test the whole local request/response path without the physical device and without a live Hermes API Server.

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

Expected response:

```text
Hermes fake mode is working. I received: check my local model server
```

This proves the bridge, auth path, request model, response model, script path, and local CLI simulator all work before the device arrives.

## Run against live Hermes

The bridge expects the Hermes API Server to expose an OpenAI-compatible endpoint at `/v1/chat/completions`.

Default live settings:

```bash
HERMES_API_BASE_URL=http://127.0.0.1:8642/v1
HERMES_API_KEY=local
HERMES_API_MODEL=hermes-agent
HERMES_OPERATOR_TOKEN=dev-token
```

Start the live bridge:

```bash
source .venv/bin/activate
export HERMES_API_KEY=dev-token
export HERMES_OPERATOR_TOKEN=dev-token
./scripts/run_bridge_live.sh
```

Call it locally:

```bash
export HERMES_OPERATOR_TOKEN=dev-token
python -m hermes_operator.cli "Say hello in one short sentence."
```

Manual curl:

```bash
curl -X POST http://127.0.0.1:8787/run \
  -H 'content-type: application/json' \
  -H "Authorization: Bearer $HERMES_OPERATOR_TOKEN" \
  -d '{"task":"Say hello in one short sentence"}'
```

If `HERMES_OPERATOR_TOKEN` is not set on the bridge, the authorization header is not required.

## Package for OpenHome

Create the custom ability zip:

```bash
./scripts/package_ability.sh
```

Default output:

```text
/tmp/hermes-operator-openhome-ability.zip
```

The zip contains the `hermes-operator/` ability folder only:

```text
hermes-operator/
hermes-operator/main.py
hermes-operator/README.md
```

Upload this zip in the OpenHome dashboard when the device/account is available.

## OpenHome runtime config

Use the LAN-accessible bridge URL for the device. On the DGX Spark LAN setup:

```bash
OPENHOME_HERMES_BRIDGE_URL=http://192.168.1.201:8787/run
OPENHOME_HERMES_BRIDGE_TOKEN=dev-token
OPENHOME_HERMES_TIMEOUT=240
```

Keep the Hermes API Server private on localhost when possible. Expose only the small bridge to the LAN.

## API

Bridge endpoint:

```text
POST /run
```

Request:

```json
{
  "task": "check my local model server",
  "session_id": "optional-session-id"
}
```

Response:

```json
{
  "ok": true,
  "spoken_summary": "Hermes fake mode is working. I received: check my local model server",
  "raw_text": "Hermes fake mode is working. I received: check my local model server",
  "artifact_path": null
}
```

## Safety model

- Bridge auth is optional but recommended on LAN.
- The OpenHome ability asks for confirmation before sending a spoken task.
- Dangerous actions should still rely on Hermes approval/safety settings.
- The bridge strips markdown/code fences and trims long responses before TTS.
- Secrets are passed through environment variables and are not committed.
- The OpenHome ability resumes normal flow on every exit path.

## Pre-device validation checklist

Run this from the repo root:

```bash
source .venv/bin/activate
pip install -e '.[dev]'
python -m pytest tests -v
python -m build
./scripts/package_ability.sh
```

Then smoke-test fake mode:

```bash
./scripts/run_bridge_fake.sh
```

In another terminal:

```bash
export HERMES_OPERATOR_TOKEN=dev-token
./scripts/demo_curl.sh "start the LAN game server and tell me the URL"
python -m hermes_operator.cli "start the LAN game server and tell me the URL"
```

If these pass, the project is ready for the physical OpenHome device step.

## More docs

- `docs/architecture.md` explains the component model and security boundary.
- `docs/pre-device-wiring.md` is the step-by-step local runbook.
- `docs/openhome-application.md` contains the DevKit application pitch.
- `openhome_ability/hermes-operator/README.md` documents the ability folder itself.

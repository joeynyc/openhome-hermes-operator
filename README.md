# OpenHome Hermes Operator

Voice bridge between OpenHome Abilities and Hermes Agent.

Goal: make an OpenHome DevKit act as a local-first voice interface for Hermes Agent and open-source models.

## Concept

OpenHome provides the microphone, speaker, trigger phrase, and voice interaction.
Hermes provides the agent runtime: tools, memory, skills, local model routing, terminal access, smart-home control, GitHub workflows, cron jobs, and web research.

## MVP Flow

1. User triggers the OpenHome ability: "Hermes operator" or "Jetson".
2. Ability asks what Hermes should do.
3. User speaks a task.
4. Ability optionally asks for confirmation.
5. Ability sends the task to a local Hermes bridge/API.
6. Hermes performs the task.
7. Ability speaks a concise voice-safe summary.

## Ability

`openhome_ability/hermes-operator/main.py`

This ability follows OpenHome's `MatchingCapability` + `CapabilityWorker` pattern and calls a local bridge endpoint.

## Bridge

`bridge/`

A small FastAPI service that accepts OpenHome ability requests and forwards them to Hermes Agent through the Hermes API Server OpenAI-compatible endpoint: `/v1/chat/completions`.

## Local Dev

```bash
cd /home/zerocool/projects/openhome-hermes-operator
python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
uvicorn hermes_operator.app:app --reload --host 0.0.0.0 --port 8787
```

Smoke test:

```bash
curl -X POST http://127.0.0.1:8787/run \
  -H 'content-type: application/json' \
  -d '{"task":"Say hello in one short sentence"}'
```

Run tests:

```bash
python3 -m pytest tests -v
```

## Safety

The first version will use allowlisted task modes and confirmations for actions that may change local state.

Dangerous tasks should not run silently by voice.

## Public Demo Target

"Jetson, check my local model server, run a quick benchmark, and tell me if anything crashed."

Expected result: OpenHome speaks a short status summary from Hermes.

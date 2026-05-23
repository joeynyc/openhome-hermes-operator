# Architecture

OpenHome Hermes Operator connects OpenHome voice hardware to Hermes Agent.

```text
User voice
  ↓
OpenHome DevKit
  ↓
OpenHome Ability: hermes-operator
  ↓ HTTP POST /run
Local Hermes Operator Bridge, FastAPI
  ↓ OpenAI-compatible /v1/chat/completions
Hermes Agent API Server
  ↓
Hermes tools, skills, memory, local models, smart-home integrations
  ↓
Concise text result
  ↓
OpenHome Ability speaks result
```

## Components

### OpenHome Ability

Path: `openhome_ability/hermes-operator/main.py`

Responsibilities:

- Capture the spoken task.
- Confirm before sending work to Hermes.
- Send the task to the bridge.
- Speak `spoken_summary`.
- Always call `resume_normal_flow()`.

### Bridge

Path: `bridge/hermes_operator/`

Responsibilities:

- Validate request shape.
- Optionally require a bearer token with `HERMES_OPERATOR_TOKEN`.
- Support fake mode with `HERMES_OPERATOR_FAKE_MODE=true`.
- Forward tasks to Hermes API Server.
- Convert Hermes output into a voice-safe summary.

### Hermes Agent

Hermes handles real work:

- terminal commands
- Docker/server checks
- GitHub workflows
- web research
- local model routing
- smart-home control
- cron jobs
- memory and skills

## Security model

The bridge is intended to run on a trusted LAN or localhost.

If `HERMES_OPERATOR_TOKEN` is set, `/run` requires:

```text
Authorization: Bearer <token>
```

The OpenHome ability sends `OPENHOME_HERMES_BRIDGE_TOKEN` as the bearer token.

Dangerous operations should still be confirmed in voice and should rely on Hermes' own approval/safety settings.

## Fake mode

For demos before Hermes API Server is available:

```bash
HERMES_OPERATOR_FAKE_MODE=true uvicorn hermes_operator.app:app --host 0.0.0.0 --port 8787
```

Then:

```bash
./scripts/demo_curl.sh "check server"
```

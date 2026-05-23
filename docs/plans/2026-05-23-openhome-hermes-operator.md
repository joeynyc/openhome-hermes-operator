# OpenHome Hermes Operator Implementation Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** Build a working OpenHome Ability + local bridge that sends spoken tasks to Hermes Agent and speaks back concise results.

**Architecture:** Keep the OpenHome ability thin. It only handles voice flow, confirmation, request formatting, and response speech. A local FastAPI bridge owns Hermes API calls, task validation, summary shaping, and local dev/test mode.

**Tech Stack:** Python 3.10+, FastAPI, httpx, pytest, OpenHome Ability SDK pattern, Hermes API Server/webhook.

---

## Task 1: Create bridge request/response models

**Objective:** Define stable JSON contracts between OpenHome ability and the local Hermes bridge.

**Files:**
- Create: `bridge/hermes_operator/models.py`
- Create: `tests/test_models.py`

**Behavior:**
- `OperatorRequest` requires `task`.
- `OperatorResponse` contains `ok`, `spoken_summary`, optional `raw_text`, optional `artifact_path`.
- Empty or whitespace-only tasks are rejected.

**Test command:**
`python -m pytest tests/test_models.py -v`

---

## Task 2: Add Hermes client abstraction

**Objective:** Add a client that can call Hermes API Server and a fake client for tests.

**Files:**
- Create: `bridge/hermes_operator/client.py`
- Create: `tests/test_client.py`

**Behavior:**
- Sends user task to `POST /v1/chat/completions`.
- Uses configurable base URL, API key, and model name.
- Extracts assistant response text from OpenAI-compatible response.
- Raises a clear `HermesClientError` on non-200 or malformed responses.

**Test command:**
`python -m pytest tests/test_client.py -v`

---

## Task 3: Add voice-safe summarizer utility

**Objective:** Ensure Hermes responses are short and speakable.

**Files:**
- Create: `bridge/hermes_operator/voice.py`
- Create: `tests/test_voice.py`

**Behavior:**
- Strip markdown/code fences.
- Collapse whitespace.
- Limit response length for voice.
- Preserve useful URLs and LAN addresses.

**Test command:**
`python -m pytest tests/test_voice.py -v`

---

## Task 4: Build FastAPI bridge endpoint

**Objective:** Create `/run` endpoint for the OpenHome ability.

**Files:**
- Create: `bridge/hermes_operator/app.py`
- Create: `tests/test_app.py`

**Behavior:**
- `POST /run` accepts `OperatorRequest`.
- Calls Hermes client.
- Returns `OperatorResponse`.
- Health endpoint returns status.

**Test command:**
`python -m pytest tests/test_app.py -v`

---

## Task 5: Create OpenHome ability scaffold

**Objective:** Add an OpenHome-compatible ability folder that calls the bridge.

**Files:**
- Create: `openhome_ability/hermes-operator/main.py`
- Create: `openhome_ability/hermes-operator/README.md`

**Behavior:**
- Extends `MatchingCapability`.
- Uses `CapabilityWorker`.
- Asks user for task.
- Confirms before running.
- Calls local bridge.
- Speaks `spoken_summary`.
- Always calls `resume_normal_flow()` on exit.

**Manual verification:**
Zip `openhome_ability/hermes-operator/`, upload to OpenHome dashboard, set trigger phrase, test in Live Editor.

---

## Task 6: Add local dev runner and docs

**Objective:** Make it easy to run the bridge locally.

**Files:**
- Create: `pyproject.toml`
- Create: `.env.example`
- Modify: `README.md`

**Commands:**
- `python -m venv .venv`
- `source .venv/bin/activate`
- `pip install -e '.[dev]'`
- `uvicorn hermes_operator.app:app --reload --host 0.0.0.0 --port 8787`

---

## Task 7: Integration smoke test with Hermes

**Objective:** Verify bridge can call a running Hermes API Server.

**Prereq:** Hermes API Server enabled with `API_SERVER_ENABLED=true`.

**Command:**
`curl -X POST http://127.0.0.1:8787/run -H 'content-type: application/json' -d '{"task":"Say hello in one short sentence"}'`

**Expected:**
JSON response with `ok: true` and short `spoken_summary`.

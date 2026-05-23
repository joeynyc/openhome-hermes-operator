# OpenHome DevKit Application Notes

## Project

Hermes Operator: a local-first OpenHome Ability that turns the DevKit into a physical voice interface for Hermes Agent and open-source models.

## Short pitch

I am building an OpenHome Ability that lets a user speak a real-world task, send it to Hermes Agent, and hear the result back through the OpenHome DevKit. OpenHome provides the voice hardware and conversational flow. Hermes provides the agent runtime: tools, memory, skills, local model routing, web research, shell/Docker access, GitHub workflows, smart-home control, and scheduled automations.

The goal is to demonstrate OpenHome as a voice interface for useful open agents, not just a chatbot.

## What the prototype already includes

- Public repo: https://github.com/joeynyc/openhome-hermes-operator
- OpenHome ability scaffold under `openhome_ability/hermes-operator/`
- Local FastAPI bridge under `bridge/hermes_operator/`
- Request/response models
- Hermes API Server client
- Voice-safe response cleanup
- Optional bearer token protection
- Fake mode for demos before live Hermes wiring
- Automated tests
- GitHub Actions CI

## Example interaction

User:

"Jetson, check my local model server, run a quick benchmark, and tell me if anything crashed."

Flow:

1. OpenHome captures the request.
2. The Hermes Operator ability asks for confirmation.
3. The ability sends the task to the local bridge.
4. The bridge forwards it to Hermes Agent.
5. Hermes checks services/logs/model endpoints and runs the benchmark.
6. The bridge returns a concise spoken summary.
7. OpenHome speaks the result.

Example response:

"The Qwen server is running. The benchmark averaged 38 tokens per second. I found no crash entries in the latest logs."

## Why this fits OpenHome

OpenHome Abilities are for actions an LLM cannot do by prompt alone: call APIs, control devices, persist data, run workflows, and create real voice experiences. Hermes Operator directly builds on that model by connecting OpenHome to a full open-source agent runtime.

This shows OpenHome as the physical voice layer for local-first agents that can operate developer tools, smart-home systems, and local AI infrastructure.

## Planned demos

1. Fake-mode bridge demo showing the OpenHome ability flow.
2. Live Hermes API Server demo with a simple spoken task.
3. Local AI lab demo: check model server, inspect logs, run benchmark.
4. Developer workflow demo: create a GitHub issue or run a test suite by voice.
5. Smart-home demo: route a spoken request through Hermes to Home Assistant/OpenHue.

## Public build commitment

I will document the build publicly with repo updates, architecture notes, demo clips, and model tests. If the integration matures, I will adapt it for contribution to the OpenHome abilities repo as a community ability.

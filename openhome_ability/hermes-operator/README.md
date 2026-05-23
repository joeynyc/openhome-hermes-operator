# Hermes Operator OpenHome Ability

This ability forwards spoken tasks to a local Hermes Operator bridge and speaks back the result.

## Trigger phrase ideas

- Hermes operator
- Jetson
- ask my lab
- run an agent task

## Runtime config

Set these for the OpenHome runtime if supported:

```bash
OPENHOME_HERMES_BRIDGE_URL=http://YOUR_BRIDGE_HOST:8787/run
OPENHOME_HERMES_BRIDGE_TOKEN=optional-shared-token
OPENHOME_HERMES_TIMEOUT=240
```

## Flow

1. Ask user what Hermes should do.
2. Wait for full transcription.
3. Confirm before sending.
4. POST to bridge.
5. Speak `spoken_summary`.
6. Resume normal OpenHome flow.

## Upload

Zip this folder and upload it in the OpenHome dashboard as a custom ability.

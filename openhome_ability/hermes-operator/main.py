"""OpenHome Ability: Hermes Operator

Thin voice interface that forwards tasks to a local Hermes Operator bridge.

Configure in OpenHome dashboard with trigger phrases such as:
- hermes operator
- jetson
- ask my lab
- run an agent task
"""

import os

import requests
from src.agent.capability import MatchingCapability
from src.agent.capability_worker import CapabilityWorker
from src.main import AgentWorker

BRIDGE_URL = os.getenv("OPENHOME_HERMES_BRIDGE_URL", "http://127.0.0.1:8787/run")
BRIDGE_TOKEN = os.getenv("OPENHOME_HERMES_BRIDGE_TOKEN", "")
REQUEST_TIMEOUT_SECONDS = int(os.getenv("OPENHOME_HERMES_TIMEOUT", "240"))
EXIT_WORDS = {"stop", "cancel", "exit", "quit", "never mind", "nothing"}


class HermesOperatorCapability(MatchingCapability):
    worker: AgentWorker = None
    capability_worker: CapabilityWorker = None

    # Do not change following tag of register capability
    #{{register capability}}

    def call(self, worker: AgentWorker):
        self.worker = worker
        self.capability_worker = CapabilityWorker(self)
        self.worker.session_tasks.create(self.run())

    async def run(self):
        try:
            await self.capability_worker.speak("What do you want Hermes to do?")
            task = await self.capability_worker.wait_for_complete_transcription()
            task = (task or "").strip()

            if not task:
                await self.capability_worker.speak("I didn't catch the task. Try again when you're ready.")
                return

            lowered = task.lower()
            if lowered in EXIT_WORDS or any(lowered.startswith(f"{word} ") for word in EXIT_WORDS):
                await self.capability_worker.speak("Okay, cancelled.")
                return

            confirmed = await self.capability_worker.run_confirmation_loop("Want me to send that to Hermes now?")
            if not confirmed:
                await self.capability_worker.speak("Okay, I won't run it.")
                return

            await self.capability_worker.speak("Sending that to Hermes. I'll report back when it finishes.")
            result = self._call_bridge(task)

            if not result.get("ok"):
                await self.capability_worker.speak(
                    result.get("spoken_summary") or "Hermes could not complete that task."
                )
                return

            await self.capability_worker.speak(result.get("spoken_summary") or "Hermes finished the task.")

        except Exception as err:
            self.worker.editor_logging_handler.error(f"[HermesOperator] unexpected error: {err}")
            await self.capability_worker.speak("Something went wrong while talking to Hermes.")
        finally:
            self.capability_worker.resume_normal_flow()

    def _call_bridge(self, task: str) -> dict:
        headers = {"Content-Type": "application/json"}
        if BRIDGE_TOKEN:
            headers["Authorization"] = f"Bearer {BRIDGE_TOKEN}"

        response = requests.post(
            BRIDGE_URL,
            headers=headers,
            json={"task": task, "session_id": "openhome-voice"},
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        return response.json()

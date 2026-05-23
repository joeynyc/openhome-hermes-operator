import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
BRIDGE = ROOT / "bridge"
if str(BRIDGE) not in sys.path:
    sys.path.insert(0, str(BRIDGE))


@pytest.fixture(autouse=True)
def clear_operator_env(monkeypatch):
    """Keep tests independent from a developer's local bridge environment."""
    for name in (
        "HERMES_OPERATOR_TOKEN",
        "HERMES_OPERATOR_FAKE_MODE",
        "HERMES_API_BASE_URL",
        "HERMES_API_KEY",
        "HERMES_API_MODEL",
    ):
        monkeypatch.delenv(name, raising=False)

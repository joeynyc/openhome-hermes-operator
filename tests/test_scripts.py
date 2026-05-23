from __future__ import annotations

import subprocess
from pathlib import Path


def test_shell_scripts_have_valid_syntax() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    scripts = sorted((repo_root / "scripts").glob("*.sh"))

    assert scripts, "expected at least one shell script"

    for script in scripts:
        result = subprocess.run(
            ["bash", "-n", str(script)],
            cwd=repo_root,
            text=True,
            capture_output=True,
            check=False,
        )
        assert result.returncode == 0, f"{script} failed bash -n: {result.stderr}"

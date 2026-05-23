import argparse
import json
import os
import sys
import urllib.error
import urllib.request


def build_headers(token: str | None) -> dict[str, str]:
    headers = {"content-type": "application/json"}
    token = (token or "").strip()
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def make_payload(task: str, session_id: str) -> dict[str, str]:
    return {"task": task, "session_id": session_id}


def summarize_response(body: str) -> str:
    data = json.loads(body)
    return data.get("spoken_summary") or data.get("raw_text") or "No spoken summary returned."


def post_task(bridge_url: str, task: str, token: str = "", session_id: str = "openhome-local") -> str:
    payload = json.dumps(make_payload(task, session_id)).encode("utf-8")
    request = urllib.request.Request(
        bridge_url,
        data=payload,
        headers=build_headers(token),
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=300) as response:
        return response.read().decode("utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Local OpenHome Hermes Operator simulator")
    parser.add_argument("task", nargs="*", help="Task to send to Hermes")
    parser.add_argument("--bridge-url", default=os.getenv("OPENHOME_HERMES_BRIDGE_URL", "http://127.0.0.1:8787/run"))
    parser.add_argument("--token", default=os.getenv("OPENHOME_HERMES_BRIDGE_TOKEN", os.getenv("HERMES_OPERATOR_TOKEN", "")))
    parser.add_argument("--session-id", default="openhome-local")
    args = parser.parse_args(argv)

    task = " ".join(args.task).strip()
    if not task:
        task = input("What do you want Hermes to do? ").strip()
    if not task:
        print("No task provided.", file=sys.stderr)
        return 2

    try:
        body = post_task(args.bridge_url, task, token=args.token, session_id=args.session_id)
    except urllib.error.HTTPError as exc:
        print(exc.read().decode("utf-8", "replace"), file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"Could not reach bridge: {exc}", file=sys.stderr)
        return 1

    print(summarize_response(body))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

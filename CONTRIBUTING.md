# Contributing

Thanks for checking out OpenHome Hermes Operator.

## Development setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
```

## Quality bar

Before opening a PR, run:

```bash
python -m pytest tests -v
python -m build
./scripts/package_ability.sh
```

## Pull requests

Keep PRs focused and use conventional commit-style titles:

```text
feat: add live bridge health check
fix: sanitize markdown links before TTS
docs: clarify OpenHome upload steps
```

For behavior changes, add or update tests. Keep the OpenHome ability thin; put testable logic in the bridge package.

## Security

Do not commit API keys, bridge tokens, device credentials, local IP secrets, or generated `.env` files.

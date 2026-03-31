# Contributing

## Development setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

## Local checks

```bash
ruff check .
pytest
```

## Prompt authoring guidelines

- Use stable namespaced IDs such as `support/refund_request`
- Increment semantic versions for every meaningful prompt revision
- Keep changelog entries short and explicit
- Declare every prompt variable in the `variables` block
- Add or update eval cases when prompt behavior changes

## Versioning guidance

- Patch: wording or formatting changes with no major behavioral intent change
- Minor: new instructions, new variables, or expanded task framing
- Major: structural prompt redesign or incompatible variable changes

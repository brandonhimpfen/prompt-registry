# prompt-registry

A versioned prompt library with evals for Python teams.

`prompt-registry` helps you store prompts as versioned artifacts, load them from disk, compare revisions, render them with variables, and run lightweight evaluations against expected behaviors.

It is designed for teams who want a simple, inspectable workflow for prompt development without depending on a database or a hosted prompt platform.

## Features

- Versioned prompt files in YAML.
- Prompt metadata, tags, owners, and changelogs.
- Variable validation for required inputs.
- Prompt rendering with safe placeholder checking.
- Registry loader for folders of prompts.
- Semantic prompt references like `support/refund_request@1.2.0`.
- Evals with exact, contains, regex, and callable checks.
- Snapshot-style regression testing for prompt outputs.
- Simple CLI for listing, showing, diffing, and evaluating prompts.
- Pure Python project with low friction local adoption.

## Install

```bash
pip install -e .
```

## Quick start

Create a prompt file:

```yaml
id: support/refund_request
version: 1.0.0
name: Refund Request Triage
owners:
  - Brandon Himpfen
summary: Triage a customer refund request and decide next action.
variables:
  customer_name:
    description: Customer full name
    required: true
  order_id:
    description: Order identifier
    required: true
  message:
    description: Customer message body
    required: true
prompt:
  system: |
    You are a careful support operations assistant.
    Review the refund request and recommend the next step.
  user: |
    Customer: {customer_name}
    Order ID: {order_id}
    Message: {message}
changelog:
  - version: 1.0.0
    date: 2026-03-31
    notes: Initial prompt.
```

Load and render it:

```python
from prompt_registry import PromptRegistry

registry = PromptRegistry.from_path("prompts")
prompt = registry.get("support/refund_request@1.0.0")
rendered = prompt.render(
    customer_name="Taylor Smith",
    order_id="ORD-1042",
    message="My package arrived damaged and I want a refund.",
)

print(rendered.system)
print(rendered.user)
```

Run evals:

```bash
python -m prompt_registry.cli eval --prompts prompts --evals examples/evals/support_refund_request.yaml
```

## Prompt file format

Each prompt is a YAML file with this basic structure:

```yaml
id: namespace/name
version: 1.0.0
name: Human readable name
owners:
  - Team or owner
summary: One-line summary
variables:
  variable_name:
    description: What this value means
    required: true
prompt:
  system: |
    System prompt text with {variables}
  user: |
    User prompt text with {variables}
metadata:
  model_family: gpt
  risk_level: low
  use_case: support
changelog:
  - version: 1.0.0
    date: 2026-03-31
    notes: Initial release.
```

## Evals format

Evals are YAML files with named test cases:

```yaml
prompt: support/refund_request@1.0.0
cases:
  - id: asks_for_decision
    input:
      customer_name: Taylor Smith
      order_id: ORD-1042
      message: My package arrived damaged and I want a refund.
    assertions:
      - type: contains
        target: user
        value: Taylor Smith
      - type: contains
        target: user
        value: ORD-1042
```

## CLI

List prompts:

```bash
python -m prompt_registry.cli list --prompts prompts
```

Show a prompt:

```bash
python -m prompt_registry.cli show --prompts prompts --ref support/refund_request@1.0.0
```

Diff two prompt versions:

```bash
python -m prompt_registry.cli diff --prompts prompts \
  --left support/refund_request@1.0.0 \
  --right support/refund_request@1.1.0
```

Evaluate prompt cases:

```bash
python -m prompt_registry.cli eval --prompts prompts --evals examples/evals/support_refund_request.yaml
```

## Project structure

```text
prompt-registry/
├── docs/
├── examples/
├── prompts/
├── src/prompt_registry/
├── tests/
├── pyproject.toml
└── README.md
```

## Why this repo exists

This project is useful when you want prompt engineering to behave more like software engineering:

- prompts live in version control.
- revisions are explicit.
- diffs are readable.
- tests are repeatable.
- teams can review prompt changes before shipping them.

## License

MIT

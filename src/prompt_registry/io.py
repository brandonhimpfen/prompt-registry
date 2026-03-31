from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .exceptions import PromptValidationError
from .models import PromptDefinition


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise PromptValidationError(f"Expected a YAML object in {path}")
    return data


def load_prompt_file(path: Path) -> PromptDefinition:
    return PromptDefinition.from_dict(load_yaml(path), source_path=str(path))

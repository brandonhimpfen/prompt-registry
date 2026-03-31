from __future__ import annotations

import difflib
import re
from pathlib import Path
from typing import Iterable

SEMVER_RE = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")


def parse_semver(value: str) -> tuple[int, int, int]:
    match = SEMVER_RE.match(value)
    if not match:
        raise ValueError(f"Invalid semantic version: {value}")
    return tuple(int(part) for part in match.groups())


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def unified_diff(left: str, right: str, left_name: str, right_name: str) -> str:
    return "\n".join(
        difflib.unified_diff(
            left.splitlines(),
            right.splitlines(),
            fromfile=left_name,
            tofile=right_name,
            lineterm="",
        )
    )


def find_placeholders(text: str) -> set[str]:
    return set(re.findall(r"\{([a-zA-Z_][a-zA-Z0-9_]*)\}", text))


def ensure_iterable(value: Iterable[str] | None) -> list[str]:
    return list(value) if value else []

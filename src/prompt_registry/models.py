from __future__ import annotations

from dataclasses import dataclass, field
from string import Formatter
from typing import Any

from .exceptions import PromptRenderError, PromptValidationError
from .utils import find_placeholders, parse_semver


@dataclass(slots=True)
class VariableSpec:
    description: str = ""
    required: bool = True
    default: Any = None


@dataclass(slots=True)
class ChangelogEntry:
    version: str
    date: str
    notes: str


@dataclass(slots=True)
class RenderedPrompt:
    id: str
    version: str
    system: str
    user: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class PromptDefinition:
    id: str
    version: str
    name: str
    owners: list[str]
    summary: str
    system: str
    user: str
    variables: dict[str, VariableSpec] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
    changelog: list[ChangelogEntry] = field(default_factory=list)
    source_path: str | None = None

    def __post_init__(self) -> None:
        try:
            parse_semver(self.version)
        except ValueError as exc:
            raise PromptValidationError(str(exc)) from exc

        if not self.id or "/" not in self.id:
            raise PromptValidationError("Prompt id must be namespaced, e.g. 'team/name'.")

        if not self.name:
            raise PromptValidationError("Prompt name is required.")

        declared = set(self.variables.keys())
        used = find_placeholders(self.system) | find_placeholders(self.user)
        unknown = used - declared
        if unknown:
            raise PromptValidationError(
                f"Prompt uses undeclared variables: {', '.join(sorted(unknown))}"
            )

    @property
    def ref(self) -> str:
        return f"{self.id}@{self.version}"

    def render(self, **kwargs: Any) -> RenderedPrompt:
        values: dict[str, Any] = {}
        for name, spec in self.variables.items():
            if name in kwargs:
                values[name] = kwargs[name]
            elif spec.default is not None:
                values[name] = spec.default
            elif spec.required:
                raise PromptRenderError(f"Missing required variable: {name}")
            else:
                values[name] = ""

        try:
            system = self.system.format(**values)
            user = self.user.format(**values)
        except KeyError as exc:
            raise PromptRenderError(f"Missing variable during render: {exc}") from exc
        except ValueError as exc:
            raise PromptRenderError(f"Invalid prompt format string: {exc}") from exc

        return RenderedPrompt(
            id=self.id,
            version=self.version,
            system=system,
            user=user,
            metadata=self.metadata,
        )

    def to_text_block(self) -> str:
        header = [
            f"ID: {self.id}",
            f"Version: {self.version}",
            f"Name: {self.name}",
            f"Owners: {', '.join(self.owners)}",
            f"Summary: {self.summary}",
            "",
            "[system]",
            self.system,
            "",
            "[user]",
            self.user,
        ]
        return "\n".join(header)

    @classmethod
    def from_dict(cls, data: dict[str, Any], source_path: str | None = None) -> "PromptDefinition":
        prompt_block = data.get("prompt") or {}
        variables = {
            name: VariableSpec(**spec)
            for name, spec in (data.get("variables") or {}).items()
        }
        changelog = [ChangelogEntry(**entry) for entry in data.get("changelog", [])]
        return cls(
            id=data["id"],
            version=data["version"],
            name=data["name"],
            owners=list(data.get("owners", [])),
            summary=data.get("summary", ""),
            system=prompt_block.get("system", ""),
            user=prompt_block.get("user", ""),
            variables=variables,
            metadata=dict(data.get("metadata", {})),
            changelog=changelog,
            source_path=source_path,
        )

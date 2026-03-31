from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .exceptions import PromptNotFoundError, PromptValidationError
from .io import load_prompt_file
from .models import PromptDefinition
from .utils import parse_semver


@dataclass
class PromptRegistry:
    prompts: dict[str, dict[str, PromptDefinition]] = field(default_factory=dict)

    def add(self, prompt: PromptDefinition) -> None:
        bucket = self.prompts.setdefault(prompt.id, {})
        if prompt.version in bucket:
            raise PromptValidationError(f"Duplicate prompt version detected: {prompt.ref}")
        bucket[prompt.version] = prompt

    @classmethod
    def from_path(cls, root: str | Path) -> "PromptRegistry":
        root_path = Path(root)
        registry = cls()
        for path in sorted(root_path.rglob("*.yaml")):
            prompt = load_prompt_file(path)
            registry.add(prompt)
        return registry

    def list_refs(self) -> list[str]:
        refs: list[str] = []
        for prompt_id in sorted(self.prompts):
            for version in self.versions(prompt_id):
                refs.append(f"{prompt_id}@{version}")
        return refs

    def ids(self) -> list[str]:
        return sorted(self.prompts.keys())

    def versions(self, prompt_id: str) -> list[str]:
        versions = self.prompts.get(prompt_id, {})
        return [v for v in sorted(versions, key=parse_semver)]

    def latest(self, prompt_id: str) -> PromptDefinition:
        versions = self.versions(prompt_id)
        if not versions:
            raise PromptNotFoundError(f"No prompt found for id: {prompt_id}")
        return self.prompts[prompt_id][versions[-1]]

    def get(self, ref: str) -> PromptDefinition:
        if "@" in ref:
            prompt_id, version = ref.split("@", 1)
            prompt = self.prompts.get(prompt_id, {}).get(version)
            if not prompt:
                raise PromptNotFoundError(f"Prompt not found: {ref}")
            return prompt
        return self.latest(ref)

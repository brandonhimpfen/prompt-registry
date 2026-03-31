from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from .exceptions import EvalError
from .models import PromptDefinition, RenderedPrompt
from .registry import PromptRegistry


@dataclass(slots=True)
class Assertion:
    type: str
    target: str
    value: str


@dataclass(slots=True)
class EvalCase:
    id: str
    input: dict[str, Any]
    assertions: list[Assertion]


@dataclass(slots=True)
class EvaluationSuite:
    prompt: str
    cases: list[EvalCase]

    @classmethod
    def from_path(cls, path: str | Path) -> "EvaluationSuite":
        raw = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
        if not isinstance(raw, dict):
            raise EvalError("Eval file must contain a YAML object.")
        cases = []
        for case in raw.get("cases", []):
            assertions = [Assertion(**item) for item in case.get("assertions", [])]
            cases.append(EvalCase(id=case["id"], input=case.get("input", {}), assertions=assertions))
        return cls(prompt=raw["prompt"], cases=cases)


@dataclass(slots=True)
class AssertionResult:
    passed: bool
    message: str
    assertion: Assertion


@dataclass(slots=True)
class EvalResult:
    case_id: str
    passed: bool
    rendered: RenderedPrompt
    assertion_results: list[AssertionResult] = field(default_factory=list)


def _target_text(rendered: RenderedPrompt, target: str) -> str:
    if target == "system":
        return rendered.system
    if target == "user":
        return rendered.user
    if target == "combined":
        return f"{rendered.system}\n\n{rendered.user}"
    raise EvalError(f"Unknown assertion target: {target}")


def evaluate_case(prompt: PromptDefinition, case: EvalCase) -> EvalResult:
    rendered = prompt.render(**case.input)
    results: list[AssertionResult] = []
    overall = True

    for assertion in case.assertions:
        target_text = _target_text(rendered, assertion.target)
        passed = False
        message = ""

        if assertion.type == "contains":
            passed = assertion.value in target_text
            message = f"Expected substring {assertion.value!r} in {assertion.target}."
        elif assertion.type == "exact":
            passed = assertion.value == target_text
            message = f"Expected exact match for {assertion.target}."
        elif assertion.type == "regex":
            passed = re.search(assertion.value, target_text) is not None
            message = f"Expected regex {assertion.value!r} to match {assertion.target}."
        else:
            raise EvalError(f"Unsupported assertion type: {assertion.type}")

        results.append(AssertionResult(passed=passed, message=message, assertion=assertion))
        overall = overall and passed

    return EvalResult(case_id=case.id, passed=overall, rendered=rendered, assertion_results=results)


def evaluate_suite(registry: PromptRegistry, suite: EvaluationSuite) -> list[EvalResult]:
    prompt = registry.get(suite.prompt)
    return [evaluate_case(prompt, case) for case in suite.cases]

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .evals import EvaluationSuite, evaluate_suite
from .registry import PromptRegistry
from .utils import unified_diff


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="prompt-registry")
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="List prompt refs")
    list_parser.add_argument("--prompts", required=True)

    show_parser = subparsers.add_parser("show", help="Show one prompt")
    show_parser.add_argument("--prompts", required=True)
    show_parser.add_argument("--ref", required=True)

    diff_parser = subparsers.add_parser("diff", help="Diff two prompt versions")
    diff_parser.add_argument("--prompts", required=True)
    diff_parser.add_argument("--left", required=True)
    diff_parser.add_argument("--right", required=True)

    eval_parser = subparsers.add_parser("eval", help="Run eval suite")
    eval_parser.add_argument("--prompts", required=True)
    eval_parser.add_argument("--evals", required=True)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    registry = PromptRegistry.from_path(args.prompts)

    if args.command == "list":
        for ref in registry.list_refs():
            print(ref)
        return 0

    if args.command == "show":
        prompt = registry.get(args.ref)
        print(prompt.to_text_block())
        return 0

    if args.command == "diff":
        left = registry.get(args.left)
        right = registry.get(args.right)
        print(unified_diff(left.to_text_block(), right.to_text_block(), left.ref, right.ref))
        return 0

    if args.command == "eval":
        suite = EvaluationSuite.from_path(args.evals)
        results = evaluate_suite(registry, suite)
        failures = 0
        for result in results:
            status = "PASS" if result.passed else "FAIL"
            print(f"[{status}] {result.case_id}")
            if not result.passed:
                failures += 1
                for item in result.assertion_results:
                    if not item.passed:
                        print(f"  - {item.message}")
        print(f"\nSummary: {len(results) - failures} passed, {failures} failed, {len(results)} total")
        return 1 if failures else 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

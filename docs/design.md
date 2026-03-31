# Design notes

## Philosophy

This project treats prompts as plain files, not hidden configuration.

That means:

- prompts can be code reviewed.
- versions can be compared with diffs.
- ownership and changelogs can be captured next to the prompt.
- simple evals can run in CI before prompt changes are merged.

## Why YAML

YAML is readable enough for prompt authors and structured enough for tooling.

## Why file-based evals

Many teams do not need a full benchmark harness on day one. File-based evals provide a strong baseline:

- they are versionable.
- they are easy to review.
- they work in CI.
- they can grow into model-backed evals later.

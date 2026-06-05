# Agent Instructions

This repository builds evidence-bound maintainer tooling. Keep output conservative and reviewable.

## Rules

- Do not invent stars, downloads, users, contributors, or maintainer status.
- Separate observed facts from manual claims.
- Prefer standard-library code unless a dependency removes substantial complexity.
- Keep CLI output stable and covered by tests.
- Update README, docs, and tests when user-facing packet sections change.

## Validation

Run:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
PYTHONPATH=src python3 -m codex_oss_maintainer_kit --help
PYTHONPATH=src python3 -m codex_oss_maintainer_kit demo --out-dir docs/examples
```

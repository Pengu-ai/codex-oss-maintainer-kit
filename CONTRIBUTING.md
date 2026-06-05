# Contributing

Thanks for helping improve Codex OSS Maintainer Kit.

## Good First Contributions

- Add parser support for another package registry.
- Improve packet wording for maintainers outside Python and JavaScript.
- Add examples from real repositories with maintainer permission.
- Add tests for edge cases in Git history parsing.

## Local Setup

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -e ".[dev]"
PYTHONPATH=src python3 -m unittest discover -s tests
```

## Pull Request Expectations

- Keep generated claims evidence-bound.
- Add or update tests for behavior changes.
- Update README or docs when user-facing output changes.
- Do not add network calls unless they are optional and documented.

## Maintainer Review Policy

All pull requests are reviewed by a maintainer before merge. Generated output, prompts, and examples must be checked for unsupported claims.

# Changelog

## 0.2.1 - 2026-06-05

- Fixed README install instructions to point at the public GitHub repository before PyPI publication.
- Renamed the GitHub issue counter field to `open_issues_and_prs_count` to avoid implying issue-only semantics.
- Normalized release metadata in JSON output instead of storing full GitHub release API payloads.
- Refreshed self-dogfood evidence after public issues and release creation.
- Replaced version-specific generated launch-plan text with next-release wording.

## 0.2.0 - 2026-06-05

- Added optional GitHub enrichment through `gh` for stars, forks, open issues, merged PRs, closed issues, releases, license, branch, and push metadata.
- Added JSON output with `--format json`.
- Added explicit `packet` command while preserving the original positional CLI.
- Added `demo` command and checked-in Markdown/JSON example outputs.
- Updated CI to validate the standard-library test suite and CLI help.

## 0.1.0 - 2026-06-05

- Initial CLI for generating maintainer evidence packets from local Git history.
- Added conservative application draft sections with TODO markers for unsupported claims.
- Added contributor guide, security policy, issue templates, and CI workflow.
- Added Codex for OSS application playbook.

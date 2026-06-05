# Codex OSS Maintainer Kit

Generate evidence packets and Codex-ready workflow plans for open-source maintainers.

This project helps maintainers turn repository activity into a clear, reviewable packet:

- repository snapshot
- active maintenance evidence
- maintainer workload notes
- ecosystem importance TODOs
- Codex workflow plan
- API credit use plan
- application draft fields for maintainer-support programs

The tool is intentionally conservative. It does not invent adoption, stars, downloads, maintainer status, or ecosystem importance. Missing evidence is marked as `TODO` so maintainers can fill it with real public links.

## Install

```bash
python -m pip install codex-oss-maintainer-kit
```

For local development:

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -e ".[dev]"
```

## Usage

Run it against any local Git repository:

```bash
codex-oss-kit /path/to/repo \
  --repo-url https://github.com/owner/repo \
  --maintainer "@your-handle" \
  --out maintainer-packet.md
```

Without installation:

```bash
python -m codex_oss_maintainer_kit /path/to/repo --out maintainer-packet.md
```

## Why This Exists

Open-source maintainers often need to explain the work that happens around code: review load, issue triage, releases, security fixes, and contributor onboarding. Those signals are scattered across Git, GitHub, package registries, and project docs.

This kit creates a structured starting point that maintainers can verify, edit, and attach to funding, grant, security, or contributor-support workflows.

## Principles

- Evidence first: generated packets separate observed Git facts from manual claims.
- Maintainer review: no generated output should be submitted without human review.
- No artificial growth: do not buy, trade, or coordinate misleading stars.
- Public links: important claims should point to issues, PRs, releases, downloads, dependents, or docs.

## Roadmap

- GitHub issue and PR enrichment through `gh` or GitHub API.
- npm, PyPI, crates.io, and Docker download signal collection.
- Release-note generation from merged PRs.
- Security-triage packet generation.
- `AGENTS.md` templates for recurring maintainer workflows.

## Development

```bash
python -m pytest
python -m codex_oss_maintainer_kit . --out examples/self-packet.md
```

## License

MIT

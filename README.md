# Codex OSS Maintainer Kit

Generate evidence-bound maintainer packets for open-source repositories.

This project helps maintainers turn repository activity into a clear, reviewable packet:

- repository snapshot
- active maintenance evidence
- maintainer workload notes
- ecosystem importance TODOs
- optional application draft fields for maintainer-support programs

The tool is intentionally conservative. It does not invent adoption, stars, downloads, maintainer status, or ecosystem importance. Missing evidence is marked as `TODO` so maintainers can fill it with real public links.

## Install

Install from GitHub:

```bash
python -m pip install "git+https://github.com/Pengu-ai/codex-oss-maintainer-kit.git"
```

For local development from a clone:

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

The explicit subcommand form is also supported:

```bash
codex-oss-kit packet /path/to/repo --out maintainer-packet.md
```

Collect GitHub public signals with `gh`:

```bash
codex-oss-kit packet /path/to/repo \
  --repo-url https://github.com/owner/repo \
  --github \
  --out maintainer-packet.md
```

Append application-draft fields only when you are preparing a reviewed application:

```bash
codex-oss-kit packet /path/to/repo \
  --repo-url https://github.com/owner/repo \
  --github \
  --application-draft \
  --out maintainer-application-draft.md
```

Write machine-readable JSON:

```bash
codex-oss-kit packet /path/to/repo \
  --format json \
  --out maintainer-profile.json
```

Generate sample outputs:

```bash
codex-oss-kit demo --out-dir docs/examples
```

Without installation:

```bash
python -m codex_oss_maintainer_kit /path/to/repo --out maintainer-packet.md
```

## Outputs

- Markdown packet: [demo-maintainer-packet.md](docs/examples/demo-maintainer-packet.md)
- JSON profile: [demo-profile.json](docs/examples/demo-profile.json)
- Self-dogfood packet: [self-maintainer-packet.md](docs/self-maintainer-packet.md)
- Self-dogfood JSON: [self-profile.json](docs/self-profile.json)

The GitHub enrichment reads public signals through `gh`: stars, forks, the GitHub open issues/PRs counter, recent merged pull requests, recent closed issues, recent releases, license, default branch, and latest push time. If `gh` is missing, unauthenticated, or offline, the packet keeps going and records collection warnings.

Generated packets do not claim that a repository enables a specific product workflow unless you opt into the application draft and then edit it with real evidence.

## Why This Exists

Open-source maintainers often need to explain the work that happens around code: review load, issue triage, releases, security fixes, and contributor onboarding. Those signals are scattered across Git, GitHub, package registries, and project docs.

This kit creates a structured starting point that maintainers can verify, edit, and attach to funding, grant, security, or contributor-support workflows.

## Principles

- Evidence first: generated packets separate observed Git facts from manual claims.
- Maintainer review: no generated output should be submitted without human review.
- No artificial growth: do not buy, trade, or coordinate misleading stars.
- Public links: important claims should point to issues, PRs, releases, downloads, dependents, or docs.

## Roadmap

- npm, PyPI, crates.io, and Docker download signal collection.
- Release-note generation from merged PRs.
- Security-triage packet generation.
- `AGENTS.md` templates for recurring maintainer workflows.

## Development

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
PYTHONPATH=src python3 -m codex_oss_maintainer_kit . --github --application-draft --out docs/self-maintainer-packet.md
PYTHONPATH=src python3 -m codex_oss_maintainer_kit demo --out-dir docs/examples
```

## License

MIT

from __future__ import annotations

import argparse
from dataclasses import replace
from pathlib import Path
import sys

from .demo import build_demo_profile
from .git_inspector import inspect_repository
from .github_inspector import collect_github_signals
from .render import render_packet
from .serialize import render_json


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="codex-oss-kit",
        description="Generate an OSS maintainer evidence packet from a local Git repository.",
        epilog="Commands: `packet` is the default command; use `demo --out-dir docs/examples` to write sample outputs.",
    )
    parser.add_argument(
        "repo",
        nargs="?",
        default=".",
        help="Path to the local Git repository to inspect.",
    )
    parser.add_argument(
        "--repo-url",
        default=None,
        help="Public GitHub repository URL to show in the packet. Defaults to origin remote.",
    )
    parser.add_argument(
        "--project-name",
        default=None,
        help="Human-readable project name. Defaults to the repository directory name.",
    )
    parser.add_argument(
        "--maintainer",
        default=None,
        help="Primary maintainer name or GitHub username.",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=90,
        help="Activity window in days for commit and file-change evidence.",
    )
    parser.add_argument(
        "--out",
        default=None,
        help="Write the packet to this Markdown file instead of stdout.",
    )
    parser.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
        help="Output format. Defaults to markdown.",
    )
    parser.add_argument(
        "--github",
        action="store_true",
        help="Enrich the packet with public GitHub signals using `gh`.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    if argv and argv[0] == "demo":
        return _run_demo(argv[1:])
    if argv and argv[0] == "packet":
        argv = argv[1:]
    parser = build_parser()
    args = parser.parse_args(argv)

    repo_path = Path(args.repo).expanduser().resolve()
    profile = inspect_repository(
        repo_path=repo_path,
        repo_url=args.repo_url,
        project_name=args.project_name,
        maintainer=args.maintainer,
        days=args.days,
    )
    if args.github:
        profile = replace(
            profile,
            github=collect_github_signals(profile.repo_url, args.days),
        )
    output = render_json(profile) if args.format == "json" else render_packet(profile)

    if args.out:
        out_path = Path(args.out).expanduser().resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(output, encoding="utf-8")
    else:
        print(output, end="")
    return 0


def _run_demo(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="codex-oss-kit demo",
        description="Write demo Markdown and JSON packet examples.",
    )
    parser.add_argument(
        "--out-dir",
        default="docs/examples",
        help="Directory to write demo files into. Defaults to docs/examples.",
    )
    args = parser.parse_args(argv)

    out_dir = Path(args.out_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    profile = build_demo_profile()
    (out_dir / "demo-maintainer-packet.md").write_text(
        render_packet(profile),
        encoding="utf-8",
    )
    (out_dir / "demo-profile.json").write_text(render_json(profile), encoding="utf-8")
    print(f"Wrote demo examples to {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

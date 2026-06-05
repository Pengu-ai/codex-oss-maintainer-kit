from __future__ import annotations

import argparse
from pathlib import Path

from .git_inspector import inspect_repository
from .render import render_packet


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="codex-oss-kit",
        description="Generate an OSS maintainer evidence packet from a local Git repository.",
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
    return parser


def main(argv: list[str] | None = None) -> int:
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
    packet = render_packet(profile)

    if args.out:
        out_path = Path(args.out).expanduser().resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(packet, encoding="utf-8")
    else:
        print(packet)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

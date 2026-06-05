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
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    packet_parser = subparsers.add_parser(
        "packet",
        help="Generate a maintainer evidence packet.",
    )
    packet_parser.add_argument(
        "repo",
        nargs="?",
        default=".",
        help="Path to the local Git repository to inspect.",
    )
    packet_parser.add_argument(
        "--repo-url",
        default=None,
        help="Public GitHub repository URL to show in the packet. Defaults to origin remote.",
    )
    packet_parser.add_argument(
        "--project-name",
        default=None,
        help="Human-readable project name. Defaults to the repository directory name.",
    )
    packet_parser.add_argument(
        "--maintainer",
        default=None,
        help="Primary maintainer name or GitHub username.",
    )
    packet_parser.add_argument(
        "--days",
        type=_positive_int,
        default=90,
        help="Activity window in days for commit and file-change evidence.",
    )
    packet_parser.add_argument(
        "--out",
        default=None,
        help="Write the packet to this Markdown file instead of stdout.",
    )
    packet_parser.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
        help="Output format. Defaults to markdown.",
    )
    packet_parser.add_argument(
        "--github",
        action="store_true",
        help="Enrich the packet with public GitHub signals using `gh`.",
    )
    packet_parser.add_argument(
        "--application-draft",
        action="store_true",
        help="Append optional application-draft fields to Markdown output.",
    )
    packet_parser.set_defaults(func=_run_packet)

    demo_parser = subparsers.add_parser(
        "demo",
        help="Write demo Markdown and JSON packet examples.",
    )
    demo_parser.add_argument(
        "--out-dir",
        default="docs/examples",
        help="Directory to write demo files into. Defaults to docs/examples.",
    )
    demo_parser.set_defaults(func=_run_demo)
    return parser


def main(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    parser = build_parser()
    try:
        args = parser.parse_args(_normalize_argv(argv))
        return args.func(args)
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


def _run_packet(args: argparse.Namespace) -> int:
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
    if args.format == "json":
        output = render_json(profile)
    else:
        output = render_packet(
            profile,
            include_application_draft=args.application_draft,
        )

    if args.out:
        out_path = Path(args.out).expanduser().resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(output, encoding="utf-8")
    else:
        print(output, end="")
    return 0


def _run_demo(args: argparse.Namespace) -> int:
    out_dir = Path(args.out_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    profile = build_demo_profile()
    (out_dir / "demo-maintainer-packet.md").write_text(
        render_packet(profile, include_application_draft=True),
        encoding="utf-8",
    )
    (out_dir / "demo-profile.json").write_text(render_json(profile), encoding="utf-8")
    print(f"Wrote demo examples to {out_dir}")
    return 0


def _normalize_argv(argv: list[str]) -> list[str]:
    if not argv:
        return ["packet"]
    if argv[0] in {"packet", "demo", "-h", "--help"}:
        return argv
    return ["packet", *argv]


def _positive_int(value: str) -> int:
    try:
        parsed = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be a positive integer") from exc
    if parsed < 1:
        raise argparse.ArgumentTypeError("must be greater than zero")
    return parsed


if __name__ == "__main__":
    raise SystemExit(main())

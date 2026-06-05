from __future__ import annotations

from datetime import date, timedelta
import json
import re
import shutil
import subprocess
from typing import Callable, Sequence

from .models import GitHubSignals

CommandRunner = Callable[[Sequence[str]], subprocess.CompletedProcess[str]]


def collect_github_signals(
    repo_url: str | None,
    days: int,
    command_runner: CommandRunner | None = None,
) -> GitHubSignals | None:
    repo_full_name = parse_github_repo(repo_url)
    if not repo_full_name:
        return GitHubSignals(
            repo_full_name=None,
            repo_html_url=repo_url,
            stars=None,
            forks=None,
            open_issues=None,
            default_branch=None,
            pushed_at=None,
            license_spdx_id=None,
            merged_pull_requests=[],
            closed_issues=[],
            recent_releases=[],
            warnings=["No GitHub owner/repo could be parsed from the repository URL."],
        )

    runner = command_runner or _run
    if command_runner is None and shutil.which("gh") is None:
        return _empty_signals(
            repo_full_name,
            f"https://github.com/{repo_full_name}",
            ["GitHub CLI (`gh`) was not found. Install and authenticate `gh` to enrich this packet."],
        )

    warnings: list[str] = []
    repo_payload = _gh_json(runner, ["gh", "api", f"repos/{repo_full_name}"], warnings)
    since = (date.today() - timedelta(days=days)).isoformat()
    prs_payload = _gh_json(
        runner,
        [
            "gh",
            "pr",
            "list",
            "-R",
            repo_full_name,
            "--state",
            "merged",
            "--limit",
            "100",
            "--search",
            f"merged:>={since}",
            "--json",
            "number,title,mergedAt,url",
        ],
        warnings,
    )
    issues_payload = _gh_json(
        runner,
        [
            "gh",
            "issue",
            "list",
            "-R",
            repo_full_name,
            "--state",
            "closed",
            "--limit",
            "100",
            "--search",
            f"closed:>={since}",
            "--json",
            "number,title,closedAt,url",
        ],
        warnings,
    )
    releases_payload = _gh_json(
        runner,
        ["gh", "api", f"repos/{repo_full_name}/releases?per_page=5"],
        warnings,
    )

    if not isinstance(repo_payload, dict):
        return _empty_signals(
            repo_full_name,
            f"https://github.com/{repo_full_name}",
            warnings or ["Repository metadata could not be fetched with `gh`."],
        )

    license_info = repo_payload.get("license") or {}
    return GitHubSignals(
        repo_full_name=repo_payload.get("full_name") or repo_full_name,
        repo_html_url=repo_payload.get("html_url") or f"https://github.com/{repo_full_name}",
        stars=_int_or_none(repo_payload.get("stargazers_count")),
        forks=_int_or_none(repo_payload.get("forks_count")),
        open_issues=_int_or_none(repo_payload.get("open_issues_count")),
        default_branch=repo_payload.get("default_branch"),
        pushed_at=repo_payload.get("pushed_at"),
        license_spdx_id=license_info.get("spdx_id") if isinstance(license_info, dict) else None,
        merged_pull_requests=_list_of_dicts(prs_payload)[:12],
        closed_issues=_list_of_dicts(issues_payload)[:12],
        recent_releases=_list_of_dicts(releases_payload)[:5],
        warnings=warnings,
    )


def parse_github_repo(repo_url: str | None) -> str | None:
    if not repo_url:
        return None
    text = repo_url.strip().rstrip("/")
    patterns = [
        r"github\.com[:/](?P<owner>[^/\s:]+)/(?P<repo>[^/\s]+?)(?:\.git)?$",
        r"^https?://api\.github\.com/repos/(?P<owner>[^/\s]+)/(?P<repo>[^/\s]+)$",
        r"^(?P<owner>[A-Za-z0-9_.-]+)/(?P<repo>[A-Za-z0-9_.-]+)$",
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            owner = match.group("owner")
            repo = match.group("repo").removesuffix(".git")
            return f"{owner}/{repo}"
    return None


def _run(args: Sequence[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(args),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def _gh_json(
    runner: CommandRunner,
    args: Sequence[str],
    warnings: list[str],
) -> object | None:
    result = runner(args)
    if result.returncode != 0:
        warnings.append(_format_command_warning(args, result.stderr))
        return None
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        warnings.append(f"`{' '.join(args[:3])}` returned invalid JSON: {exc.msg}.")
        return None


def _format_command_warning(args: Sequence[str], stderr: str) -> str:
    command = " ".join(args[:4])
    detail = stderr.strip().splitlines()[0] if stderr.strip() else "no error detail"
    return f"`{command}` failed: {detail}"


def _empty_signals(
    repo_full_name: str,
    repo_html_url: str | None,
    warnings: list[str],
) -> GitHubSignals:
    return GitHubSignals(
        repo_full_name=repo_full_name,
        repo_html_url=repo_html_url,
        stars=None,
        forks=None,
        open_issues=None,
        default_branch=None,
        pushed_at=None,
        license_spdx_id=None,
        merged_pull_requests=[],
        closed_issues=[],
        recent_releases=[],
        warnings=warnings,
    )


def _int_or_none(value: object) -> int | None:
    if isinstance(value, int):
        return value
    return None


def _list_of_dicts(value: object | None) -> list[dict[str, object]]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]

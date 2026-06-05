from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path
import subprocess


@dataclass(frozen=True)
class RepoProfile:
    project_name: str
    repo_path: Path
    repo_url: str | None
    maintainer: str | None
    branch: str | None
    latest_tag: str | None
    activity_window_days: int
    commit_count: int
    recent_commits: list[str]
    contributors: list[str]
    changed_files: list[str]
    generated_on: date


def inspect_repository(
    repo_path: Path,
    repo_url: str | None,
    project_name: str | None,
    maintainer: str | None,
    days: int,
) -> RepoProfile:
    if not repo_path.exists():
        raise FileNotFoundError(f"Repository path does not exist: {repo_path}")
    if not (repo_path / ".git").exists():
        raise ValueError(f"Path is not a Git repository: {repo_path}")

    resolved_repo_url = repo_url or _git(
        repo_path, "remote", "get-url", "origin", allow_error=True
    )
    recent_commits = _lines(
        _git(
            repo_path,
            "log",
            f"--since={days} days ago",
            "--pretty=format:%h %ad %an %s",
            "--date=short",
            allow_error=True,
        )
    )
    changed_files = _lines(
        _git(
            repo_path,
            "log",
            f"--since={days} days ago",
            "--name-only",
            "--pretty=format:",
            allow_error=True,
        )
    )
    contributors = _lines(
        _git(repo_path, "shortlog", "-sn", "--all", allow_error=True)
    )

    return RepoProfile(
        project_name=project_name or repo_path.name,
        repo_path=repo_path,
        repo_url=resolved_repo_url,
        maintainer=maintainer,
        branch=_git(repo_path, "branch", "--show-current", allow_error=True),
        latest_tag=_git(repo_path, "describe", "--tags", "--abbrev=0", allow_error=True),
        activity_window_days=days,
        commit_count=len(recent_commits),
        recent_commits=recent_commits[:12],
        contributors=contributors[:12],
        changed_files=sorted(set(changed_files))[:30],
        generated_on=date.today(),
    )


def _git(repo_path: Path, *args: str, allow_error: bool = False) -> str | None:
    result = subprocess.run(
        ["git", *args],
        cwd=repo_path,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        if allow_error:
            return None
        raise RuntimeError(result.stderr.strip() or f"git {' '.join(args)} failed")
    text = result.stdout.strip()
    return text or None


def _lines(value: str | None) -> list[str]:
    if not value:
        return []
    return [line.strip() for line in value.splitlines() if line.strip()]

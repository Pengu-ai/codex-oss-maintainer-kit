from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class GitHubSignals:
    repo_full_name: str | None
    repo_html_url: str | None
    stars: int | None
    forks: int | None
    open_issues_and_prs_count: int | None
    default_branch: str | None
    pushed_at: str | None
    license_spdx_id: str | None
    merged_pull_requests: list[dict[str, Any]]
    closed_issues: list[dict[str, Any]]
    recent_releases: list[dict[str, Any]]
    warnings: list[str]


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
    github: GitHubSignals | None = None

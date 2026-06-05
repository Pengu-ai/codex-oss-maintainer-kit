from __future__ import annotations

from .models import GitHubSignals, RepoProfile


def render_packet(profile: RepoProfile, include_application_draft: bool = False) -> str:
    repo_url = profile.repo_url or "TODO: add public GitHub URL"
    maintainer = profile.maintainer or "TODO: add maintainer name and GitHub username"
    latest_tag = _latest_tag(profile)
    branch = profile.branch or "Unknown"

    lines = [
        f"# {profile.project_name} Maintainer Evidence Packet",
        "",
        f"Generated: {profile.generated_on.isoformat()}",
        "",
        "## Repository Snapshot",
        "",
        f"- Repository: {repo_url}",
        f"- Local path: `{profile.repo_path}`",
        f"- Maintainer: {maintainer}",
        f"- Default/current branch: `{branch}`",
        f"- Latest tag/release: `{latest_tag}`",
        f"- Activity window: last {profile.activity_window_days} days",
        "",
        "## Active Maintenance Evidence",
        "",
        f"- Recent commits found: {profile.commit_count}",
        "- Recent commit examples:",
        *(_bullet_lines(profile.recent_commits) or ["  - TODO: add recent commits after first release"]),
        "- Recently touched files:",
        *(_bullet_lines(profile.changed_files) or ["  - TODO: add real maintenance activity"]),
        "- Contributors observed in Git history:",
        *(_bullet_lines(profile.contributors) or ["  - TODO: add contributors as the project grows"]),
        "",
        "## GitHub Public Signals",
        "",
        *_github_lines(profile.github),
        "",
        "## Maintainer Workload",
        "",
        "- TODO: add monthly issue volume, PR volume, review burden, release cadence, and security triage needs.",
        "- TODO: link to representative issues, pull requests, release notes, or discussions.",
        "- TODO: state whether the maintainer is primary maintainer, core maintainer, or repo admin.",
        "",
        "## Ecosystem Importance",
        "",
        "- TODO: add concrete evidence such as GitHub stars, dependent projects, package downloads, users, forks, citations, or community adoption.",
        "- TODO: explain why the project matters even if it is early: workflow category, underserved maintainer pain, or infrastructure role.",
        "",
        "## Next Evidence To Add",
        "",
        "- Public links for any claims that are not already backed by Git or GitHub data.",
        "- Release notes, dependency/download signals, security advisories, or contributor-support examples when available.",
        "- Human-written context for why the maintenance work matters.",
        "",
    ]
    if include_application_draft:
        lines.extend(_application_draft_lines())
    return "\n".join(lines)


def _bullet_lines(lines: list[str]) -> list[str]:
    return [f"  - {line}" for line in lines]


def _github_lines(github: GitHubSignals | None) -> list[str]:
    if github is None:
        return [
            "- Not collected. Re-run with `--github` and a public GitHub remote or `--repo-url`.",
        ]

    lines = [
        f"- GitHub repository: {github.repo_html_url or github.repo_full_name or 'Unknown'}",
        f"- Stars: {_value_or_todo(github.stars, 'TODO: add public adoption signal')}",
        f"- Forks: {_value_or_todo(github.forks, 'TODO: add public fork signal')}",
        f"- Open issues/PRs counter: {_value_or_todo(github.open_issues_and_prs_count, 'TODO: collect issue/PR count')}",
        f"- GitHub default branch: `{github.default_branch or 'Unknown'}`",
        f"- Last pushed at: {github.pushed_at or 'Unknown'}",
        f"- License: {github.license_spdx_id or 'Unknown'}",
        f"- Merged pull requests in window: {len(github.merged_pull_requests)}",
        f"- Closed issues in window: {len(github.closed_issues)}",
        f"- Recent releases found: {len(github.recent_releases)}",
    ]
    if github.warnings:
        lines.append("- Collection warnings:")
        lines.extend(f"  - {warning}" for warning in github.warnings)
    if github.merged_pull_requests:
        lines.append("- Recent merged pull requests:")
        lines.extend(_linked_item_lines(github.merged_pull_requests, "mergedAt"))
    if github.closed_issues:
        lines.append("- Recent closed issues:")
        lines.extend(_linked_item_lines(github.closed_issues, "closedAt"))
    if github.recent_releases:
        lines.append("- Recent releases:")
        lines.extend(_release_lines(github.recent_releases))
    return lines


def _latest_tag(profile: RepoProfile) -> str:
    if profile.latest_tag:
        return profile.latest_tag
    if profile.github and profile.github.recent_releases:
        release = profile.github.recent_releases[0]
        tag = release.get("tag_name") or release.get("tagName")
        if isinstance(tag, str) and tag:
            return tag
    return "No Git tag or GitHub release found yet"


def _application_draft_lines() -> list[str]:
    return [
        "## Application Draft",
        "",
        "### Role",
        "",
        "TODO: I am the primary/core maintainer of this public open-source repository and responsible for roadmap, reviews, releases, and contributor support.",
        "",
        "### Why this repository is eligible",
        "",
        "TODO: Replace with a 500-character evidence-based summary covering adoption, maintenance activity, and ecosystem importance.",
        "",
        "### How API credits would be used",
        "",
        "TODO: Replace with a 500-character plan for PR review, issue triage, release workflows, and maintainer automation.",
        "",
    ]


def _value_or_todo(value: int | None, fallback: str) -> str:
    if value is None:
        return fallback
    return str(value)


def _linked_item_lines(items: list[dict[str, object]], date_key: str) -> list[str]:
    lines = []
    for item in items[:5]:
        number = item.get("number", "?")
        title = item.get("title", "Untitled")
        url = item.get("url", "")
        happened_at = item.get(date_key, "unknown date")
        suffix = f" - {url}" if url else ""
        lines.append(f"  - #{number} {title} ({happened_at}){suffix}")
    return lines


def _release_lines(items: list[dict[str, object]]) -> list[str]:
    lines = []
    for item in items[:5]:
        tag = item.get("tag_name") or item.get("tagName") or "unknown tag"
        name = item.get("name") or tag
        published_at = item.get("published_at") or item.get("publishedAt") or "unknown date"
        url = item.get("html_url") or item.get("url") or ""
        suffix = f" - {url}" if url else ""
        lines.append(f"  - {tag}: {name} ({published_at}){suffix}")
    return lines

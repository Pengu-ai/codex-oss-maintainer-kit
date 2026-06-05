from __future__ import annotations

from .git_inspector import RepoProfile


def render_packet(profile: RepoProfile) -> str:
    repo_url = profile.repo_url or "TODO: add public GitHub URL"
    maintainer = profile.maintainer or "TODO: add maintainer name and GitHub username"
    latest_tag = profile.latest_tag or "No Git tag found yet"
    branch = profile.branch or "Unknown"

    return "\n".join(
        [
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
            f"- Latest tag: `{latest_tag}`",
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
            "## Codex Workflows This Project Enables",
            "",
            "- Generate review briefs for incoming pull requests before maintainer review.",
            "- Convert Git history and issue activity into release checklists.",
            "- Produce triage prompts that preserve maintainer context and avoid stale assumptions.",
            "- Build repeatable maintainer packets for funding, security review, or contributor onboarding.",
            "",
            "## API Credit Use Plan",
            "",
            "- Batch summarize issue and pull request context for maintainers.",
            "- Generate release-note drafts from merged pull requests and commit history.",
            "- Run recurring quality checks on docs, onboarding, and maintainer handoff packets.",
            "- Keep all generated output reviewable before publication or repository changes.",
            "",
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
            "## 30-Day Public Launch Plan",
            "",
            "- Publish the repository with an MIT license, clear README, examples, and issue templates.",
            "- Cut v0.1.0 and create a changelog entry.",
            "- Dogfood the CLI on 3-5 real public repositories with maintainer permission.",
            "- Open good-first-issue tasks for parser support, GitHub API enrichment, and docs examples.",
            "- Collect adoption evidence without artificial stars or misleading claims.",
            "",
        ]
    )


def _bullet_lines(lines: list[str]) -> list[str]:
    return [f"  - {line}" for line in lines]

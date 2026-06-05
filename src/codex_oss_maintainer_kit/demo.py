from __future__ import annotations

from datetime import date
from pathlib import Path

from .models import GitHubSignals, RepoProfile


def build_demo_profile() -> RepoProfile:
    return RepoProfile(
        project_name="demo-maintainer-project",
        repo_path=Path("/path/to/demo-maintainer-project"),
        repo_url="https://github.com/example/demo-maintainer-project",
        maintainer="@example-maintainer",
        branch="main",
        latest_tag="v0.3.0",
        activity_window_days=90,
        commit_count=18,
        recent_commits=[
            "a1b2c3d 2026-06-02 Example Maintainer Fix release checklist",
            "d4e5f6a 2026-05-28 Example Maintainer Review contributor docs",
            "f7a8b9c 2026-05-20 Example Maintainer Add security triage notes",
        ],
        contributors=[
            "12\tExample Maintainer",
            "3\tExternal Contributor",
        ],
        changed_files=[
            ".github/workflows/ci.yml",
            "CHANGELOG.md",
            "README.md",
            "SECURITY.md",
            "src/demo_project/release.py",
            "tests/test_release.py",
        ],
        generated_on=date.today(),
        github=GitHubSignals(
            repo_full_name="example/demo-maintainer-project",
            repo_html_url="https://github.com/example/demo-maintainer-project",
            stars=128,
            forks=17,
            open_issues_and_prs_count=6,
            default_branch="main",
            pushed_at="2026-06-05T02:00:00Z",
            license_spdx_id="MIT",
            merged_pull_requests=[
                {
                    "number": 42,
                    "title": "Add release checklist",
                    "mergedAt": "2026-06-01T12:00:00Z",
                    "url": "https://github.com/example/demo-maintainer-project/pull/42",
                },
                {
                    "number": 39,
                    "title": "Improve contributor onboarding",
                    "mergedAt": "2026-05-24T09:00:00Z",
                    "url": "https://github.com/example/demo-maintainer-project/pull/39",
                },
            ],
            closed_issues=[
                {
                    "number": 31,
                    "title": "Document security report flow",
                    "closedAt": "2026-05-29T18:00:00Z",
                    "url": "https://github.com/example/demo-maintainer-project/issues/31",
                }
            ],
            recent_releases=[
                {
                    "tag_name": "v0.3.0",
                    "name": "v0.3.0",
                    "published_at": "2026-06-03T00:00:00Z",
                    "html_url": "https://github.com/example/demo-maintainer-project/releases/tag/v0.3.0",
                }
            ],
            warnings=[],
        ),
    )

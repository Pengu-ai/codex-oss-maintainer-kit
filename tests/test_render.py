from pathlib import Path
from datetime import date
import unittest

from codex_oss_maintainer_kit.models import GitHubSignals, RepoProfile
from codex_oss_maintainer_kit.render import render_packet


class RenderPacketTests(unittest.TestCase):
    def test_render_packet_stays_evidence_bound_by_default(self) -> None:
        profile = RepoProfile(
            project_name="demo",
            repo_path=Path("/tmp/demo"),
            repo_url="https://github.com/example/demo",
            maintainer="@example",
            branch="main",
            latest_tag="v0.1.0",
            activity_window_days=90,
            commit_count=2,
            recent_commits=["abc123 2026-06-01 A Fix parser"],
            contributors=["1\tA"],
            changed_files=["src/demo.py"],
            generated_on=date(2026, 6, 5),
        )

        packet = render_packet(profile)

        self.assertIn("# demo Maintainer Evidence Packet", packet)
        self.assertNotIn("## Application Draft", packet)
        self.assertNotIn("## Codex Workflows This Project Enables", packet)
        self.assertIn("https://github.com/example/demo", packet)

    def test_render_packet_can_include_application_draft_when_requested(self) -> None:
        profile = RepoProfile(
            project_name="demo",
            repo_path=Path("/tmp/demo"),
            repo_url="https://github.com/example/demo",
            maintainer="@example",
            branch="main",
            latest_tag="v0.1.0",
            activity_window_days=90,
            commit_count=2,
            recent_commits=["abc123 2026-06-01 A Fix parser"],
            contributors=["1\tA"],
            changed_files=["src/demo.py"],
            generated_on=date(2026, 6, 5),
        )

        packet = render_packet(profile, include_application_draft=True)

        self.assertIn("## Application Draft", packet)

    def test_render_packet_marks_missing_adoption_as_todo(self) -> None:
        profile = RepoProfile(
            project_name="early",
            repo_path=Path("/tmp/early"),
            repo_url=None,
            maintainer=None,
            branch=None,
            latest_tag=None,
            activity_window_days=30,
            commit_count=0,
            recent_commits=[],
            contributors=[],
            changed_files=[],
            generated_on=date(2026, 6, 5),
        )

        packet = render_packet(profile)

        self.assertIn("TODO: add public GitHub URL", packet)
        self.assertIn("TODO: add concrete evidence", packet)
        self.assertIn("No Git tag or GitHub release found yet", packet)

    def test_render_packet_uses_github_release_when_local_tag_missing(self) -> None:
        profile = RepoProfile(
            project_name="release-only",
            repo_path=Path("/tmp/release-only"),
            repo_url="https://github.com/example/release-only",
            maintainer="@example",
            branch="main",
            latest_tag=None,
            activity_window_days=90,
            commit_count=1,
            recent_commits=["abc123 2026-06-01 A Release"],
            contributors=["1\tA"],
            changed_files=["CHANGELOG.md"],
            generated_on=date(2026, 6, 5),
            github=GitHubSignals(
                repo_full_name="example/release-only",
                repo_html_url="https://github.com/example/release-only",
                stars=1,
                forks=0,
                open_issues_and_prs_count=0,
                default_branch="main",
                pushed_at="2026-06-05T00:00:00Z",
                license_spdx_id="MIT",
                merged_pull_requests=[],
                closed_issues=[],
                recent_releases=[
                    {
                        "tag_name": "v1.0.0",
                        "name": "v1.0.0",
                        "published_at": "2026-06-05T00:00:00Z",
                        "html_url": "https://github.com/example/release-only/releases/tag/v1.0.0",
                    }
                ],
                warnings=[],
            ),
        )

        packet = render_packet(profile)

        self.assertIn("Latest tag/release: `v1.0.0`", packet)


if __name__ == "__main__":
    unittest.main()

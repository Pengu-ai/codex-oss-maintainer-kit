from datetime import date
from pathlib import Path
import json
import unittest

from codex_oss_maintainer_kit.models import GitHubSignals, RepoProfile
from codex_oss_maintainer_kit.serialize import render_json


class SerializeTests(unittest.TestCase):
    def test_render_json_serializes_dates_paths_and_github_signals(self) -> None:
        profile = RepoProfile(
            project_name="demo",
            repo_path=Path("/tmp/demo"),
            repo_url="https://github.com/owner/repo",
            maintainer="@owner",
            branch="main",
            latest_tag=None,
            activity_window_days=90,
            commit_count=0,
            recent_commits=[],
            contributors=[],
            changed_files=[],
            generated_on=date(2026, 6, 5),
            github=GitHubSignals(
                repo_full_name="owner/repo",
                repo_html_url="https://github.com/owner/repo",
                stars=1,
                forks=2,
                open_issues=3,
                default_branch="main",
                pushed_at="2026-06-05T00:00:00Z",
                license_spdx_id="MIT",
                merged_pull_requests=[],
                closed_issues=[],
                recent_releases=[],
                warnings=[],
            ),
        )

        payload = json.loads(render_json(profile))

        self.assertEqual(payload["repo_path"], "/tmp/demo")
        self.assertEqual(payload["generated_on"], "2026-06-05")
        self.assertEqual(payload["github"]["stars"], 1)


if __name__ == "__main__":
    unittest.main()

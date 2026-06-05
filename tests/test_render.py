from pathlib import Path
from datetime import date
import unittest

from codex_oss_maintainer_kit.git_inspector import RepoProfile
from codex_oss_maintainer_kit.render import render_packet


class RenderPacketTests(unittest.TestCase):
    def test_render_packet_includes_application_sections(self) -> None:
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
        self.assertIn("## Application Draft", packet)
        self.assertIn("## Codex Workflows This Project Enables", packet)
        self.assertIn("https://github.com/example/demo", packet)

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
        self.assertIn("No Git tag found yet", packet)


if __name__ == "__main__":
    unittest.main()

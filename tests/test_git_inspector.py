from pathlib import Path
import subprocess
import unittest

from tempfile import TemporaryDirectory

from codex_oss_maintainer_kit.git_inspector import inspect_repository


class GitInspectorTests(unittest.TestCase):
    def test_inspect_repository_reads_git_history_and_tags(self) -> None:
        with TemporaryDirectory() as temp_dir:
            repo = Path(temp_dir)
            _git(repo, "init")
            _git(repo, "config", "user.name", "Example Maintainer")
            _git(repo, "config", "user.email", "maintainer@example.com")
            (repo / "README.md").write_text("# Demo\n", encoding="utf-8")
            _git(repo, "add", "README.md")
            _git(repo, "commit", "-m", "Initial commit")
            _git(repo, "tag", "v0.1.0")

            profile = inspect_repository(
                repo_path=repo,
                repo_url="https://github.com/example/demo",
                project_name=None,
                maintainer="@example",
                days=90,
            )

            self.assertEqual(profile.project_name, repo.name)
            self.assertEqual(profile.repo_url, "https://github.com/example/demo")
            self.assertEqual(profile.latest_tag, "v0.1.0")
            self.assertEqual(profile.commit_count, 1)
            self.assertIn("README.md", profile.changed_files)
            self.assertTrue(any("Example Maintainer" in item for item in profile.contributors))


def _git(repo: Path, *args: str) -> None:
    subprocess.run(
        ["git", *args],
        cwd=repo,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )


if __name__ == "__main__":
    unittest.main()

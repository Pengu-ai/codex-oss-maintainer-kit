import subprocess
import unittest

from codex_oss_maintainer_kit.github_inspector import (
    collect_github_signals,
    parse_github_repo,
)


class GitHubInspectorTests(unittest.TestCase):
    def test_parse_github_repo_accepts_common_urls(self) -> None:
        self.assertEqual(
            parse_github_repo("https://github.com/owner/repo.git"),
            "owner/repo",
        )
        self.assertEqual(parse_github_repo("https://github.com/owner/repo/"), "owner/repo")
        self.assertEqual(parse_github_repo("git@github.com:owner/repo.git"), "owner/repo")
        self.assertEqual(parse_github_repo("owner/repo"), "owner/repo")

    def test_collect_github_signals_uses_runner_payloads(self) -> None:
        def runner(args: list[str]) -> subprocess.CompletedProcess[str]:
            command = " ".join(args)
            if command.startswith("gh api repos/owner/repo/releases"):
                stdout = '[{"tag_name":"v0.1.0","name":"first","published_at":"2026-06-01","html_url":"https://github.com/owner/repo/releases/tag/v0.1.0"}]'
            elif command.startswith("gh api repos/owner/repo"):
                stdout = '{"full_name":"owner/repo","html_url":"https://github.com/owner/repo","stargazers_count":42,"forks_count":7,"open_issues_count":3,"default_branch":"main","pushed_at":"2026-06-05T00:00:00Z","license":{"spdx_id":"MIT"}}'
            elif command.startswith("gh pr list"):
                stdout = '[{"number":12,"title":"Add parser","mergedAt":"2026-06-02T00:00:00Z","url":"https://github.com/owner/repo/pull/12"}]'
            elif command.startswith("gh issue list"):
                stdout = '[{"number":4,"title":"Fix docs","closedAt":"2026-06-03T00:00:00Z","url":"https://github.com/owner/repo/issues/4"}]'
            else:
                stdout = "{}"
            return subprocess.CompletedProcess(args, 0, stdout=stdout, stderr="")

        signals = collect_github_signals(
            "https://github.com/owner/repo",
            days=90,
            command_runner=runner,
        )

        self.assertIsNotNone(signals)
        assert signals is not None
        self.assertEqual(signals.stars, 42)
        self.assertEqual(signals.forks, 7)
        self.assertEqual(signals.open_issues, 3)
        self.assertEqual(len(signals.merged_pull_requests), 1)
        self.assertEqual(len(signals.closed_issues), 1)
        self.assertEqual(len(signals.recent_releases), 1)


if __name__ == "__main__":
    unittest.main()

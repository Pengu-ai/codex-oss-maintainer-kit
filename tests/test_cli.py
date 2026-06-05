import unittest

from contextlib import redirect_stderr
import io
from pathlib import Path
from tempfile import TemporaryDirectory

from codex_oss_maintainer_kit.cli import build_parser, main


class CliTests(unittest.TestCase):
    def test_packet_command_defaults_to_current_directory(self) -> None:
        args = build_parser().parse_args(["packet"])

        self.assertEqual(args.command, "packet")
        self.assertEqual(args.repo, ".")
        self.assertEqual(args.days, 90)
        self.assertIsNone(args.out)
        self.assertEqual(args.format, "markdown")
        self.assertFalse(args.github)
        self.assertFalse(args.application_draft)

    def test_cli_accepts_json_and_github_flags(self) -> None:
        args = build_parser().parse_args(["packet", ".", "--format", "json", "--github"])

        self.assertEqual(args.format, "json")
        self.assertTrue(args.github)

    def test_demo_command_writes_markdown_and_json_examples(self) -> None:
        with TemporaryDirectory() as temp_dir:
            exit_code = main(["demo", "--out-dir", temp_dir])

            self.assertEqual(exit_code, 0)
            self.assertTrue(Path(temp_dir, "demo-maintainer-packet.md").exists())
            self.assertTrue(Path(temp_dir, "demo-profile.json").exists())

    def test_cli_returns_friendly_error_for_non_git_path(self) -> None:
        with TemporaryDirectory() as temp_dir:
            stderr = io.StringIO()
            with redirect_stderr(stderr):
                exit_code = main([temp_dir])

            self.assertEqual(exit_code, 2)
            self.assertIn("error:", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()

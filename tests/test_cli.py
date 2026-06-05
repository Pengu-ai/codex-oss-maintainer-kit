import unittest

from pathlib import Path
from tempfile import TemporaryDirectory

from codex_oss_maintainer_kit.cli import build_parser, main


class CliTests(unittest.TestCase):
    def test_cli_defaults_to_current_directory(self) -> None:
        args = build_parser().parse_args([])

        self.assertEqual(args.repo, ".")
        self.assertEqual(args.days, 90)
        self.assertIsNone(args.out)
        self.assertEqual(args.format, "markdown")
        self.assertFalse(args.github)

    def test_cli_accepts_json_and_github_flags(self) -> None:
        args = build_parser().parse_args([".", "--format", "json", "--github"])

        self.assertEqual(args.format, "json")
        self.assertTrue(args.github)

    def test_demo_command_writes_markdown_and_json_examples(self) -> None:
        with TemporaryDirectory() as temp_dir:
            exit_code = main(["demo", "--out-dir", temp_dir])

            self.assertEqual(exit_code, 0)
            self.assertTrue(Path(temp_dir, "demo-maintainer-packet.md").exists())
            self.assertTrue(Path(temp_dir, "demo-profile.json").exists())


if __name__ == "__main__":
    unittest.main()

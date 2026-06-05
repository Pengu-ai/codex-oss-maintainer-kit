import unittest

from codex_oss_maintainer_kit.cli import build_parser


class CliTests(unittest.TestCase):
    def test_cli_defaults_to_current_directory(self) -> None:
        args = build_parser().parse_args([])

        self.assertEqual(args.repo, ".")
        self.assertEqual(args.days, 90)
        self.assertIsNone(args.out)


if __name__ == "__main__":
    unittest.main()

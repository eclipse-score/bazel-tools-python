"""Tests for the black runner."""

import json
import pathlib
import sys
import tempfile
import unittest
from unittest.mock import patch

from quality.private.python.tools import black_runner, python_tool_common


class TestBlackRunner(unittest.TestCase):
    """Test class for black runner."""

    def setUp(self) -> None:
        self.tmp_text_file_path = pathlib.Path(tempfile.mkstemp()[1])
        self.tmp_json_file_path = pathlib.Path(tempfile.mkstemp()[1])
        self.aspect_args = python_tool_common.AspectArguments(
            target_imports=set(),
            target_dependencies=set(),
            tool=pathlib.Path(""),
            tool_config=pathlib.Path(""),
            tool_root="",
            target_files=set(),
            tool_output_text=self.tmp_text_file_path,
            tool_output_json=self.tmp_json_file_path,
            refactor=False,
        )

    def tearDown(self) -> None:
        self.tmp_text_file_path.unlink()
        self.tmp_json_file_path.unlink()

    def test_black_removeprefix(self) -> None:
        """Test black _removeprefix for both text string cases."""
        would_reformat_message = "would reformat file.py."
        expected_text = "reformat"
        expected_strip_text = "file.py."

        # pylint: disable-next=protected-access
        return_text = black_runner._removeprefix(text=expected_text, prefix=black_runner.WOULD_REFORMAT_MSG)
        # pylint: disable-next=protected-access
        return_strip_text = black_runner._removeprefix(
            text=would_reformat_message, prefix=black_runner.WOULD_REFORMAT_MSG
        )

        assert return_text == expected_text
        assert return_strip_text == expected_strip_text

    def test_black_output_parser_with_no_issues(self) -> None:
        """Tests black_output_parser function with the results of a file with no issues."""
        expected_findings = python_tool_common.Findings()
        findings = black_runner.black_output_parser(
            python_tool_common.SubprocessInfo(
                stdout="",
                stderr="",
                return_code=0,
            )
        )

        self.assertEqual(expected_findings, findings)

    def test_get_black_command_with_refactor(self) -> None:
        """Tests get_black_command function with the refactor being true."""
        self.aspect_args.refactor = True
        command = black_runner.get_black_command(self.aspect_args)

        self.assertFalse("--diff" in command)

    def test_black_output_parser_with_issues(self) -> None:
        """Tests black_output_parser function with results of files with issues."""
        expected_findings = python_tool_common.Findings(
            [
                python_tool_common.Finding(
                    path=pathlib.Path("file.py"),
                    message="Should be reformatted.",
                    severity=python_tool_common.Severity.WARN,
                    tool="black",
                    rule_id="formatting",
                )
            ]
        )

        findings = black_runner.black_output_parser(
            python_tool_common.SubprocessInfo(
                stdout="",
                stderr="--- file.py\nwould reformat file.py\n",
                return_code=0,
            )
        )

        self.assertEqual(expected_findings, findings)

    @patch(
        "quality.private.python.tools.python_tool_common.execute_subprocess",
        side_effect=[
            python_tool_common.SubprocessInfo(
                stdout="",
                stderr="",
                return_code=0,
            )
        ],
    )
    def test_call_main(self, _) -> None:
        """Tests calling main."""
        mocked_args = [
            "--tool",
            " ",
            "--tool-config",
            " ",
            "--tool-output-text",
            str(self.tmp_text_file_path),
            "--tool-output-json",
            str(self.tmp_json_file_path),
            "--tool-root",
            " ",
        ]
        with patch.object(sys, "argv", ["black"] + mocked_args):
            black_runner.main()
            self.assertFalse(self.aspect_args.tool_output_text.read_text(encoding="utf-8"))
            self.assertFalse(json.loads(self.aspect_args.tool_output_json.read_text(encoding="utf-8")))


if __name__ == "__main__":  # pragma: no cover
    unittest.main()

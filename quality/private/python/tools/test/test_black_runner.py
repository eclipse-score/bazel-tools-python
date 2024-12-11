"""Tests for the black runner."""

import pathlib
import sys
import tempfile
import unittest
from unittest.mock import patch

from quality.private.python.tools import black_runner, python_tool_common


class TestBlackRunner(unittest.TestCase):
    """Test class for black runner."""

    def setUp(self) -> None:
        _, self.tmp_file_path = tempfile.mkstemp()
        self.aspect_args = python_tool_common.AspectArguments(
            target_imports=set(),
            target_dependencies=set(),
            tool=pathlib.Path(""),
            tool_config=pathlib.Path(""),
            tool_root="",
            target_files=set(),
            tool_output=pathlib.Path(self.tmp_file_path),
            refactor=False,
        )

    def tearDown(self) -> None:
        pathlib.Path(self.tmp_file_path).unlink()

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
    def test_black_output_with_no_issues(self, _) -> None:
        """Tests check_with_black function with the results of a file with no issues."""
        black_runner.check_with_black(self.aspect_args)

        self.assertFalse(self.aspect_args.tool_output.read_text(encoding="utf-8"))

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
    def test_black_output_with_refactor(self, execute_subprocess) -> None:
        """Tests check_with_black function with the refactor being true."""
        self.aspect_args.refactor = True
        black_runner.check_with_black(self.aspect_args)

        self.assertFalse("--diff" in execute_subprocess.call_args.args[0])

    @patch(
        "quality.private.python.tools.python_tool_common.execute_subprocess",
        side_effect=[
            python_tool_common.SubprocessInfo(
                stdout="",
                stderr="--- file.py\nwould reformat file.py",
                return_code=0,
            )
        ],
    )
    def test_black_output_with_issues(self, _) -> None:
        """Tests check_with_black function with results of files with issues."""
        expected_error_message = (
            "\nThe following findings were found:\n file.py: Should be reformatted. [black:formatting]\n"
        )
        exepected_output_message = " file.py: Should be reformatted. [black:formatting]"
        expected_output_log_message = f"INFO:root:Created black output at: {self.tmp_file_path}"
        findings = python_tool_common.Findings()
        findings += [
            python_tool_common.Finding(
                path=pathlib.Path("file.py"),
                message="Should be reformatted.",
                severity=python_tool_common.Severity.WARN,
                tool="black",
                rule_id="formatting",
            )
        ]
        with self.assertRaises(python_tool_common.LinterFindingAsError) as exception:
            with self.assertLogs() as logs:
                black_runner.check_with_black(self.aspect_args)

            output_log_message = logs.output[0]
            output_file_content = self.aspect_args.tool_output.read_text(encoding="utf-8")

            self.assertEqual(expected_error_message, str(exception.exception))
            self.assertEqual(exepected_output_message, output_file_content)
            self.assertEqual(expected_output_log_message, output_log_message)

    @patch(
        "quality.private.python.tools.python_tool_common.execute_subprocess",
        side_effect=[
            python_tool_common.LinterSubprocessError(
                commands=[],
                stdout="",
                stderr="1 file would be reformatted.",
                return_code=1,
            )
        ],
    )
    def test_check_with_black_unexpected_exception(self, _) -> None:
        """Test check_with_black function when an unexpected exception occurs."""
        with self.assertRaises(python_tool_common.LinterSubprocessError) as exception:
            with self.assertLogs() as logs:
                black_runner.check_with_black(self.aspect_args)
        self.assertEqual(exception.exception.return_code, 1)
        self.assertFalse(self.aspect_args.tool_output.read_text(encoding="utf-8"))
        self.assertFalse(logs.output)

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
            "--tool-output",
            self.tmp_file_path,
            "--tool-root",
            " ",
        ]
        with patch.object(sys, "argv", ["black"] + mocked_args):
            black_runner.main()
            self.assertFalse(self.aspect_args.tool_output.read_text(encoding="utf-8"))


if __name__ == "__main__":  # pragma: no cover
    unittest.main()

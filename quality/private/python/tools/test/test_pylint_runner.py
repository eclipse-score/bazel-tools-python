"""Tests for the pylint runner."""

import os
import pathlib
import sys
import tempfile
import unittest
from unittest.mock import patch

from quality.private.python.tools import pylint_runner, python_tool_common


class TestPylintRunner(unittest.TestCase):
    """Test class for pylint runner."""

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
    def test_pylint_output_with_no_issues(self, _) -> None:
        """Tests check_with_pylint function with the results of a file with no issues."""
        self.aspect_args.target_imports = set([pathlib.Path("termcolor")])
        pylint_runner.check_with_pylint(self.aspect_args)
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
    def test_pylint_output_with_no_issues_and_python_path_set(self, _) -> None:
        """Tests check_with_pylint function with the results of a file with no issues and PYTHONPATH variable set."""
        modified_environ = os.environ.copy()
        modified_environ["PYTHONPATH"] = "python"
        with patch.dict(os.environ, modified_environ, clear=True):
            self.aspect_args.target_imports = set([pathlib.Path("termcolor")])
            pylint_runner.check_with_pylint(self.aspect_args)
            self.assertFalse(self.aspect_args.tool_output.read_text(encoding="utf-8"))

    @patch(
        "quality.private.python.tools.python_tool_common.execute_subprocess",
        side_effect=[
            python_tool_common.LinterSubprocessError(
                commands=[],
                stdout="************* Module pylint_runner\nfile.py:11:1:Error message:error-code\n",
                stderr="",
                return_code=16,
            )
        ],
    )
    def test_pylint_output_with_issues(self, _) -> None:
        """Tests check_with_pylint function with the results of a file with issues."""
        expected_error_message = "file.py:11:1: Error message [pylint:error-code]"
        expected_output_log_message = f"INFO:root:Created pylint output at: {self.tmp_file_path}"

        with self.assertRaises(python_tool_common.LinterFindingAsError) as exception:
            with self.assertLogs() as logs:
                pylint_runner.check_with_pylint(self.aspect_args)

        findings_as_error_message = str(exception.exception.findings)
        output_file_content = self.aspect_args.tool_output.read_text(encoding="utf-8")
        output_log_message = logs.output[0]

        self.assertEqual(expected_error_message, findings_as_error_message)
        self.assertEqual(expected_error_message, output_file_content)
        self.assertEqual(expected_output_log_message, output_log_message)

    @patch(
        "quality.private.python.tools.python_tool_common.execute_subprocess",
        side_effect=[
            python_tool_common.LinterSubprocessError(
                commands=[],
                stdout="",
                stderr="ERROR: unexpected error\n",
                return_code=32,
            )
        ],
    )
    def test_check_with_pylint_unexpected_exception(self, _) -> None:
        """Test check_with_pylint function when an unexpected exception occurs."""
        with self.assertRaises(python_tool_common.LinterSubprocessError) as exception:
            with self.assertLogs() as logs:
                pylint_runner.check_with_pylint(self.aspect_args)

        expected_return_code = 32

        self.assertEqual(exception.exception.return_code, expected_return_code)
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
        with patch.object(sys, "argv", ["pylint"] + mocked_args):
            pylint_runner.main()
            self.assertFalse(self.aspect_args.tool_output.read_text(encoding="utf-8"))


if __name__ == "__main__":  # pragma: no cover
    unittest.main()

"""Tests for the isort runner."""

import pathlib
import sys
import tempfile
import unittest
from unittest.mock import patch

from quality.private.python.tools import isort_runner, python_tool_common


class TestIsortRunner(unittest.TestCase):
    """Test class for isort runner."""

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
    def test_isort_output_with_no_issues(self, _) -> None:
        """Tests check_with_isort function with the results of a file with no issues."""
        isort_runner.check_with_isort(self.aspect_args)

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
        """Tests check_with_isort function with the refactor being true."""
        self.aspect_args.refactor = True
        isort_runner.check_with_isort(self.aspect_args)

        self.assertFalse("--check-only" in execute_subprocess.call_args.args[0])
        self.assertFalse("--diff" in execute_subprocess.call_args.args[0])

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
    def test_black_output_without_refactor(self, execute_subprocess) -> None:
        """Tests check_with_isort function without the refactor being true."""
        self.aspect_args.refactor = False
        isort_runner.check_with_isort(self.aspect_args)

        self.assertTrue("--check-only" in execute_subprocess.call_args.args[0])
        self.assertTrue("--diff" in execute_subprocess.call_args.args[0])

    @patch(
        "quality.private.python.tools.python_tool_common.execute_subprocess",
        side_effect=[
            python_tool_common.LinterSubprocessError(
                commands=[],
                stdout="",
                stderr="ERROR: file.py Imports are incorrectly sorted and/or formatted.\n",
                return_code=1,
            )
        ],
    )
    def test_isort_output_with_issues(self, _) -> None:
        """Tests check_with_isort function with the results of a file with issues."""
        expected_error_message = "file.py: Imports are incorrectly sorted and/or formatted. [isort:imports_formatting]"
        expected_output_log_message = f"INFO:root:Created isort output at: {self.tmp_file_path}"
        self.aspect_args.refactor = True

        with self.assertRaises(python_tool_common.LinterFindingAsError) as exception:
            with self.assertLogs() as logs:
                isort_runner.check_with_isort(self.aspect_args)

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
                return_code=2,
            )
        ],
    )
    def test_check_with_isort_unexpected_exception(self, _) -> None:
        """Test check_with_isort function when an unexpected exception occurs."""

        with self.assertRaises(python_tool_common.LinterSubprocessError) as exception:
            with self.assertLogs() as logs:
                isort_runner.check_with_isort(self.aspect_args)

        self.assertEqual(exception.exception.return_code, 2)
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
        with patch.object(sys, "argv", ["isort"] + mocked_args):
            with patch(
                "quality.private.python.tools.python_tool_common.execute_subprocess",
                side_effect=[
                    python_tool_common.SubprocessInfo(
                        stdout="",
                        stderr="",
                        return_code=0,
                    )
                ],
            ):
                isort_runner.main()
                self.assertFalse(self.aspect_args.tool_output.read_text(encoding="utf-8"))


if __name__ == "__main__":  # pragma: no cover
    unittest.main()

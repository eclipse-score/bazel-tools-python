"""Tests for the pylint runner."""

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
            refactor=False,
        )

    def tearDown(self) -> None:
        pathlib.Path(self.tmp_file_path).unlink()

    def test_pylint_output_with_no_issues(self) -> None:
        """Tests pylint_output_parser function with the results of a file with no issues."""
        expected_findings = python_tool_common.Findings()

        findings = pylint_runner.pylint_output_parser(
            python_tool_common.SubprocessInfo(
                stdout="",
                stderr="",
                return_code=0,
            )
        )
        self.assertEqual(expected_findings, findings)

    def test_pylint_output_with_issues(self) -> None:
        """Tests pylint_output_parser function with the results of a file with issues."""
        expected_findings = python_tool_common.Findings(
            [
                python_tool_common.Finding(
                    path=pathlib.Path("file.py"),
                    message="Error message",
                    severity=python_tool_common.Severity.WARN,
                    tool="pylint",
                    rule_id="error-code",
                    line=11,
                    column=1,
                )
            ]
        )
        findings = pylint_runner.pylint_output_parser(
            python_tool_common.SubprocessInfo(
                stdout="************* Module pylint_runner\nfile.py:11:1:Error message:error-code\n",
                stderr="",
                return_code=16,
            )
        )

        self.assertEqual(expected_findings, findings)

    def test_pylint_unexpected_exception(self) -> None:
        """Test pylint_exception_handler function when an unexpected exception occurs."""
        with self.assertRaises(python_tool_common.LinterSubprocessError) as exception:
            with self.assertLogs() as logs:
                pylint_runner.pylint_exception_handler(
                    python_tool_common.LinterSubprocessError(
                        commands=[],
                        stdout="",
                        stderr="ERROR: unexpected error\n",
                        return_code=32,
                    )
                )

        expected_return_code = 32

        self.assertEqual(exception.exception.return_code, expected_return_code)
        self.assertFalse(self.aspect_args.tool_output.read_text(encoding="utf-8"))
        self.assertFalse(logs.output)

    def test_pylint_exception_handler(self) -> None:
        """Test pylint_exception_handler function when an expected exception occurs."""
        expected_info = python_tool_common.SubprocessInfo(
            stdout="stdout message",
            stderr="",
            return_code=2,
        )

        info = pylint_runner.pylint_exception_handler(
            python_tool_common.LinterSubprocessError(
                commands=[],
                stdout="stdout message",
                stderr="",
                return_code=2,
            )
        )

        self.assertEqual(expected_info, info)

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

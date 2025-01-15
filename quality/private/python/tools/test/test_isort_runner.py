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

    def test_isort_output_with_no_issues(self) -> None:
        """Tests isort_output_parser function with the results of a file with no issues."""
        expected_findings = python_tool_common.Findings()

        findings = isort_runner.isort_output_parser(
            python_tool_common.SubprocessInfo(
                stdout="",
                stderr="",
                return_code=0,
            )
        )

        self.assertEqual(expected_findings, findings)

    def test_get_isort_command_with_refactor(self) -> None:
        """Tests get_isort_command function with the refactor being true."""
        self.aspect_args.refactor = True
        command = isort_runner.get_isort_command(self.aspect_args)

        self.assertFalse("--check-only" in command)
        self.assertFalse("--diff" in command)

    def test_isort_output_with_issues(self) -> None:
        """Tests isort_output_parser function with the results of a file with issues."""
        expected_findings = python_tool_common.Findings(
            [
                python_tool_common.Finding(
                    path=pathlib.Path("file.py"),
                    message="Imports are incorrectly sorted and/or formatted.",
                    severity=python_tool_common.Severity.WARN,
                    tool="isort",
                    rule_id="imports_formatting",
                )
            ]
        )

        findings = isort_runner.isort_output_parser(
            python_tool_common.SubprocessInfo(
                stdout="",
                stderr="ERROR: file.py Imports are incorrectly sorted and/or formatted.\n",
                return_code=1,
            )
        )

        self.assertEqual(expected_findings, findings)

    def test_isort_unexpected_exception(self) -> None:
        """Test isort_exception_handler function when an unexpected exception occurs."""

        with self.assertRaises(python_tool_common.LinterSubprocessError) as exception:
            with self.assertLogs() as logs:
                isort_runner.isort_exception_handler(
                    python_tool_common.LinterSubprocessError(
                        commands=[],
                        stdout="",
                        stderr="ERROR: unexpected error\n",
                        return_code=2,
                    )
                )

        self.assertEqual(exception.exception.return_code, 2)
        self.assertFalse(self.aspect_args.tool_output.read_text(encoding="utf-8"))
        self.assertFalse(logs.output)

    def test_isort_exception_handler(self) -> None:
        """Test isort_exception_handler function when an expected exception occurs."""
        expected_info = python_tool_common.SubprocessInfo(
            stdout="stdout message",
            stderr="stderr message",
            return_code=isort_runner.ISORT_BAD_CHECK_ERROR_CODE,
        )

        info = isort_runner.isort_exception_handler(
            python_tool_common.LinterSubprocessError(
                commands=[],
                stdout="stdout message",
                stderr="stderr message",
                return_code=isort_runner.ISORT_BAD_CHECK_ERROR_CODE,
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

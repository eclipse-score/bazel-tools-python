"""Tests for the ruff_format runner."""

import pathlib

import pytest
from pytest_mock import MockerFixture

from quality.private.python.tools import python_tool_common, ruff_format_runner


@pytest.mark.parametrize(
    "subprocess_output, linter_subprocess_error",
    [
        (("", "", 0), ([], "stdout message", "", 1)),
        (("stdout message", "", 1), ([], "stdout message", "", 1)),
    ],
    indirect=["subprocess_output", "linter_subprocess_error"],
)
def test_ruff_format_output_parser_with_no_issues(
    subprocess_output: python_tool_common.SubprocessInfo,
    linter_subprocess_error: python_tool_common.LinterSubprocessError,
) -> None:
    """Tests ruff_format_output_parser function and ruff_format_exception_handler."""
    expected_findings = python_tool_common.Findings()

    if subprocess_output.return_code == 0:
        findings = ruff_format_runner.ruff_format_output_parser(subprocess_output)
        assert expected_findings == findings
    if subprocess_output.return_code == ruff_format_runner.RUFF_BAD_CHECK_ERROR_CODE:
        expection_info = ruff_format_runner.ruff_format_exception_handler(linter_subprocess_error)
        assert subprocess_output == expection_info


def test_get_ruff_format_command(aspect_args: python_tool_common.AspectArguments) -> None:
    """Tests get_ruff_format_command function return commands."""
    target_file = "".join(str(file) for file in aspect_args.target_files)
    expected_command = [
        "tool.exec",
        "format",
        "--config",
        "tool.config",
        "--diff",
        target_file,
    ]

    ruff_format_command = ruff_format_runner.get_ruff_format_command(aspect_args)

    assert ruff_format_command == expected_command


@pytest.mark.parametrize(
    "linter_subprocess_error",
    [([], "stdout message", "", 1)],
    indirect=["linter_subprocess_error"],
)
def test_ruff_format_exception_handler(
    linter_subprocess_error: python_tool_common.LinterSubprocessError,
) -> None:
    """Test ruff_format_exception_handler function when an expected exception occurs."""
    expected_info = python_tool_common.SubprocessInfo(
        stdout="stdout message",
        stderr="",
        return_code=1,
    )

    info = ruff_format_runner.ruff_format_exception_handler(linter_subprocess_error)

    assert expected_info == info


@pytest.mark.parametrize(
    "linter_subprocess_error",
    [([], "", "ERROR: unexpected error\n", 32)],
    indirect=["linter_subprocess_error"],
)
def test_ruff_format_unexpected_exception(
    linter_subprocess_error: python_tool_common.LinterSubprocessError,
) -> None:
    """Test ruff_format_exception_handler function when an unexpected exception occurs."""
    with pytest.raises(python_tool_common.LinterSubprocessError) as exception:
        ruff_format_runner.ruff_format_exception_handler(linter_subprocess_error)

    expected_exception = (
        'The command "[]" returned code "32" and the following error message:\nERROR: unexpected error\n'
    )

    assert expected_exception == str(exception.value)


@pytest.mark.parametrize(
    "subprocess_output, finding",
    [
        (
            ("stdout", "", 1),
            (
                pathlib.Path("file.py"),
                "Should be reformatted.",
                python_tool_common.Severity.WARN,
                "ruff_format",
                "formatting",
                1,
                1,
            ),
        )
    ],
    indirect=["subprocess_output", "finding"],
)
def test_ruff_format_output_parser_with_issues(
    subprocess_output: python_tool_common.SubprocessInfo, finding: python_tool_common.Finding
) -> None:
    """Tests ruff_format_output_parser function with results of files with issues."""
    expected_findings = python_tool_common.Findings([finding])

    tool_output = subprocess_output
    tool_output.stdout = (
        "--- file.py\n+++ file.py\n"
        + "@@ -9,6 +9,7 @@\n"
        + "from quality.private.python.tools import pylint_runner, python_tool_common\n"
        + "import os\n \n+\n class TestPylintRunner(unittest.TestCase):\n"
        + '"""Test class for pylint runner."""\n \n\n'
    )
    tool_output.stderr = "1 file would be reformatted\n"
    findings = ruff_format_runner.ruff_format_output_parser(tool_output)

    assert expected_findings == findings


def test_get_ruff_format_command_with_refactor(aspect_args: python_tool_common.AspectArguments) -> None:
    """Tests get_ruff_format_command function with the refactor being true."""
    aspect_args.refactor = True

    ruff_format_command = ruff_format_runner.get_ruff_format_command(aspect_args)

    assert "--diff" not in ruff_format_command


def test_call_main(mocker: MockerFixture) -> None:
    """Tests calling main."""
    execute_runner_mock = mocker.patch("quality.private.python.tools.python_tool_common.execute_runner")

    ruff_format_runner.main()

    execute_runner_mock.assert_called_once_with(
        get_command=ruff_format_runner.get_ruff_format_command,
        output_parser=ruff_format_runner.ruff_format_output_parser,
        exception_handler=ruff_format_runner.ruff_format_exception_handler,
    )

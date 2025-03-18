"""Tests for the mypy runner."""

import pathlib

import pytest
from pytest_mock import MockerFixture

from quality.private.python.tools import mypy_runner, python_tool_common


@pytest.mark.parametrize(
    "subprocess_output, linter_subprocess_error",
    [
        (("", "", 0), ([], "stdout message", "", 1)),
        (("stdout message", "", 1), ([], "stdout message", "", 1)),
    ],
    indirect=["subprocess_output", "linter_subprocess_error"],
)
def test_mypy_output_parser_with_no_issues(
    subprocess_output: python_tool_common.SubprocessInfo,
    linter_subprocess_error: python_tool_common.LinterSubprocessError,
) -> None:
    """Tests mypy_output_parser function and mypy_exception_handler."""
    expected_findings = python_tool_common.Findings()

    if subprocess_output.return_code == 0:
        findings = mypy_runner.mypy_output_parser(subprocess_output)
        assert expected_findings == findings
    if subprocess_output.return_code == mypy_runner.MYPY_BAD_CHECK_ERROR_CODE:
        expection_info = mypy_runner.mypy_exception_handler(linter_subprocess_error)
        assert subprocess_output == expection_info


def test_get_mypy_command(aspect_args: python_tool_common.AspectArguments) -> None:
    """Tests get_mypy_command function return commands."""
    target_file = "".join(str(file) for file in aspect_args.target_files)
    expected_command = [
        "tool.exec",
        "--config-file",
        "tool.config",
        "--show-column-numbers",
        target_file,
    ]

    mypy_command = mypy_runner.get_mypy_command(aspect_args)

    assert mypy_command == expected_command


@pytest.mark.parametrize(
    "linter_subprocess_error",
    [([], "", "ERROR: unexpected error\n", 32)],
    indirect=["linter_subprocess_error"],
)
def test_mypy_unexpected_exception(
    linter_subprocess_error: python_tool_common.LinterSubprocessError,
) -> None:
    """Test mypy_exception_handler function when an unexpected exception occurs."""
    with pytest.raises(python_tool_common.LinterSubprocessError) as exception:
        mypy_runner.mypy_exception_handler(linter_subprocess_error)

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
                'Unsupported operand types for + ("int" and "str")',
                python_tool_common.Severity.WARN,
                "mypy",
                "mypy:operator",
                11,
                12,
            ),
        )
    ],
    indirect=["subprocess_output", "finding"],
)
def test_mypy_output_parser_with_issues(
    subprocess_output: python_tool_common.SubprocessInfo, finding: python_tool_common.Finding
) -> None:
    """Tests mypy_output_parser function with results of files with issues."""

    expected_findings = python_tool_common.Findings([finding])

    tool_output = subprocess_output
    tool_output.stdout = (
        'file.py:11:12: error: Unsupported operand types for + ("int" and "str") [mypy:operator]\n'
        + "Found 1 error in 1 file (checked 1 source file)\n"
    )
    findings = mypy_runner.mypy_output_parser(tool_output)

    assert expected_findings == findings


def test_call_main(mocker: MockerFixture) -> None:
    """Tests calling main with mypy methods."""
    execute_runner_mock = mocker.patch("quality.private.python.tools.python_tool_common.execute_runner")

    mypy_runner.main()

    execute_runner_mock.assert_called_once_with(
        get_command=mypy_runner.get_mypy_command,
        output_parser=mypy_runner.mypy_output_parser,
        exception_handler=mypy_runner.mypy_exception_handler,
    )

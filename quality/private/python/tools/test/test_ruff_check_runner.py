"""Tests for the ruff_check runner."""

import pathlib

import pytest
from pytest_mock import MockerFixture

from quality.private.python.tools import python_tool_common, ruff_check_runner


@pytest.mark.parametrize(
    "subprocess_output, linter_subprocess_error",
    [
        (("[]", "", 0), ([], "stdout message", "", 1)),
        (("stdout message", "", 1), ([], "stdout message", "", 1)),
    ],
    indirect=["subprocess_output", "linter_subprocess_error"],
)
def test_ruff_check_output_parser_with_no_issues(
    subprocess_output: python_tool_common.SubprocessInfo,
    linter_subprocess_error: python_tool_common.LinterSubprocessError,
) -> None:
    """Tests ruff_check_output_parser function and ruff_check_exception_handler."""
    expected_findings = python_tool_common.Findings()

    if subprocess_output.return_code == 0:
        findings = ruff_check_runner.ruff_check_output_parser(subprocess_output)
        assert expected_findings == findings
    if subprocess_output.return_code == ruff_check_runner.RUFF_BAD_CHECK_ERROR_CODE:
        expection_info = ruff_check_runner.ruff_check_exception_handler(linter_subprocess_error)
        assert subprocess_output == expection_info


def test_get_ruff_check_command(aspect_args: python_tool_common.AspectArguments) -> None:
    """Tests get_ruff_check_command function return commands."""
    target_file = "".join(str(file) for file in aspect_args.target_files)
    expected_command = [
        "tool.exec",
        "check",
        "--config",
        "tool.config",
        "--unsafe-fixes",
        "--output-format",
        "json",
        target_file,
    ]

    ruff_check_command = ruff_check_runner.get_ruff_check_command(aspect_args)

    assert ruff_check_command == expected_command


@pytest.mark.parametrize(
    "linter_subprocess_error",
    [([], "stdout message", "", 1)],
    indirect=["linter_subprocess_error"],
)
def test_ruff_check_exception_handler(
    linter_subprocess_error: python_tool_common.LinterSubprocessError,
) -> None:
    """Test ruff_check_exception_handler function when an expected exception occurs."""
    expected_info = python_tool_common.SubprocessInfo(
        stdout="stdout message",
        stderr="",
        return_code=1,
    )

    info = ruff_check_runner.ruff_check_exception_handler(linter_subprocess_error)

    assert expected_info == info


@pytest.mark.parametrize(
    "linter_subprocess_error",
    [([], "", "ERROR: unexpected error\n", 32)],
    indirect=["linter_subprocess_error"],
)
def test_ruff_check_unexpected_exception(
    linter_subprocess_error: python_tool_common.LinterSubprocessError,
) -> None:
    """Test ruff_check_exception_handler function when an unexpected exception occurs."""
    with pytest.raises(python_tool_common.LinterSubprocessError) as exception:
        ruff_check_runner.ruff_check_exception_handler(linter_subprocess_error)

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
                pathlib.Path("path/file.py"),
                "`os` imported but unused",
                python_tool_common.Severity.WARN,
                "ruff_check",
                "F401",
                10,
                8,
            ),
        )
    ],
    indirect=["subprocess_output", "finding"],
)
def test_ruff_check_output_parser_with_issues(
    subprocess_output: python_tool_common.SubprocessInfo, finding: python_tool_common.Finding
) -> None:
    """Tests ruff_check_output_parser function with results of files with issues."""
    expected_findings = python_tool_common.Findings([finding])

    tool_output = subprocess_output
    tool_output.stdout = """[\n{\n
                "cell": null,\n
                "code": "F401",\n
                "end_location": {\n"column": 10,\n"row": 10\n},\n
                "filename": "path/file.py",\n
                "fix": {\n
                    "applicability": "safe",\n
                    "edits": [\n{\n"content": "",\n
                                    "end_location": {\n
                                                    "column": 1,\n
                                                    "row": 6\n
                                                    },\n
                                    "location": {\n
                                                    "column": 1,\n
                                                    "row": 5\n
                                                    }\n}\n],\n
                    "message": "Remove unused import: `os`"\n
                },\n
                "location": {\n"column":8,\n"row": 10\n},\n
                "message": "`os` imported but unused",\n
                "noqa_row": 5,\n
                "url": "https://docs.astral.sh/ruff/rules/unused-import"\n}\n]"""
    findings = ruff_check_runner.ruff_check_output_parser(tool_output)

    assert expected_findings == findings


def test_get_ruff_check_command_with_refactor(aspect_args: python_tool_common.AspectArguments) -> None:
    """Tests get_ruff_check_command function with the refactor being true."""
    aspect_args.refactor = True

    ruff_check_command = ruff_check_runner.get_ruff_check_command(aspect_args)

    assert "--fix" in ruff_check_command
    assert "--unsafe-fixes" not in ruff_check_command


def test_call_main(mocker: MockerFixture) -> None:
    """Tests calling main."""
    execute_runner_mock = mocker.patch("quality.private.python.tools.python_tool_common.execute_runner")

    ruff_check_runner.main()

    execute_runner_mock.assert_called_once_with(
        get_command=ruff_check_runner.get_ruff_check_command,
        output_parser=ruff_check_runner.ruff_check_output_parser,
        exception_handler=ruff_check_runner.ruff_check_exception_handler,
    )

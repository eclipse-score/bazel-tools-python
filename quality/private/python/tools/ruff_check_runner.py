"""A runner that interfaces python tool aspect and runs ruff on a list of files."""

import json
import pathlib
import typing as t

from quality.private.python.tools import python_tool_common

RUFF_BAD_CHECK_ERROR_CODE = 1


def get_ruff_check_command(aspect_arguments: python_tool_common.AspectArguments) -> t.List[str]:
    """Returns the command to run a ruff check subprocess."""
    subprocess_list = [
        f"{aspect_arguments.tool}",
        "check",
        "--config",
        f"{aspect_arguments.tool_config}",
        "--fix",
        "--output-format",
        "json",
        *map(str, aspect_arguments.target_files),
    ]

    if not aspect_arguments.refactor:
        subprocess_list.remove("--fix")
        subprocess_list[4:4] = ["--unsafe-fixes"]

    return subprocess_list


def ruff_check_output_parser(tool_output: python_tool_common.SubprocessInfo) -> python_tool_common.Findings:
    """Parses `tool_output` to get the findings returned from the tool execution."""
    findings = python_tool_common.Findings()

    for finding in json.loads(tool_output.stdout):
        findings.append(
            python_tool_common.Finding(
                path=pathlib.Path(finding["filename"]),
                message=finding["message"],
                severity=python_tool_common.Severity.WARN,
                tool="ruff_check",
                rule_id=finding["code"],
                line=finding["location"]["row"],
                column=finding["location"]["column"],
            )
        )

    return findings


def ruff_check_exception_handler(
    exception: python_tool_common.LinterSubprocessError,
) -> python_tool_common.SubprocessInfo:
    """Handles the cases that ruff_check has a non-zero return code."""
    if exception.return_code != RUFF_BAD_CHECK_ERROR_CODE:
        raise exception

    return python_tool_common.SubprocessInfo(
        exception.stdout,
        exception.stderr,
        exception.return_code,
    )


def main():
    """Main entry point."""
    python_tool_common.execute_runner(
        get_command=get_ruff_check_command,
        output_parser=ruff_check_output_parser,
        exception_handler=ruff_check_exception_handler,
    )


if __name__ == "__main__":  # pragma: no cover
    main()

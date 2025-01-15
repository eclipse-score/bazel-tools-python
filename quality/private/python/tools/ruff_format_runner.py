"""A runner that interfaces python tool aspect and runs ruff on a list of files."""

import pathlib
import typing as t

from quality.private.python.tools import python_tool_common

RUFF_BAD_CHECK_ERROR_CODE = 1


def get_ruff_format_command(aspect_arguments: python_tool_common.AspectArguments) -> t.List[str]:
    """Returns the command to run a ruff format subprocess."""

    subprocess_list = [
        f"{aspect_arguments.tool}",
        "format",
        "--config",
        f"{aspect_arguments.tool_config}",
        *map(str, aspect_arguments.target_files),
    ]
    if not aspect_arguments.refactor:
        subprocess_list[4:4] = ["--diff"]

    return subprocess_list


def ruff_format_output_parser(tool_output: python_tool_common.SubprocessInfo) -> python_tool_common.Findings:
    """Parses `tool_output` to get the findings returned from the tool execution."""
    findings = python_tool_common.Findings()

    files = {file.lstrip("-").strip() for file in tool_output.stdout.splitlines() if file.startswith("---")}

    for file in files:
        findings.append(
            python_tool_common.Finding(
                path=pathlib.Path(file),
                message="Should be reformatted.",
                severity=python_tool_common.Severity.WARN,
                tool="ruff_format",
                rule_id="formatting",
            )
        )

    return findings


def ruff_format_exception_handler(
    exception: python_tool_common.LinterSubprocessError,
) -> python_tool_common.SubprocessInfo:
    """Handles the cases that ruff_format has a non-zero return code."""
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
        get_command=get_ruff_format_command,
        output_parser=ruff_format_output_parser,
        exception_handler=ruff_format_exception_handler,
    )


if __name__ == "__main__":  # pragma: no cover
    main()

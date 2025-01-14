"""A runner that interfaces python tool aspect and runs pylint on a list of files."""

import logging
import pathlib

from quality.private.python.tools import python_tool_common

PYLINT_MODULE_START_MSG = "************* Module"


def is_pylint_critical_error(exception: python_tool_common.LinterSubprocessError) -> bool:
    """Checks if the return code represents a pylint critical error.

    Cases considered:
    - Pylint returns an odd number when a fatal error occurs;
    - Pylint returns 32 when an unrecognized option is used in the CLI call;
    - Pylint returns an error message in stderr when an option is configured with a invalid value.
    """
    return_code = int(exception.return_code)
    return (return_code % 2) == 1 or return_code == 32 or exception.stderr != ""


def check_with_pylint(aspect_arguments: python_tool_common.AspectArguments) -> None:
    """Run a pylint subprocess, check its output and write its findings to a file."""

    findings = python_tool_common.Findings()

    try:
        pylint_output = python_tool_common.execute_subprocess(
            [
                # Binary executable path.
                f"{aspect_arguments.tool}",
                # Configuration flag and path.
                "--rcfile",
                f"{aspect_arguments.tool_config}",
                # Text content template.
                "--msg-template",
                "{path}:{line}:{column}:{msg}:{symbol}",
                # Exclude pylint persistent output as this would be both action input and output.
                "--persistent",
                "no",
                "--score",
                "no",
                # Files to lint
                "--",
                *map(str, aspect_arguments.target_files),
            ],
        )
    except python_tool_common.LinterSubprocessError as exception:
        if is_pylint_critical_error(exception):
            raise exception

        pylint_output = python_tool_common.SubprocessInfo(
            exception.stdout,
            exception.stderr,
            exception.return_code,
        )

    for output_line in pylint_output.stdout.splitlines():
        if output_line.startswith(PYLINT_MODULE_START_MSG):
            continue

        path, line, column, message, rule_id = output_line.split(":")

        findings.append(
            python_tool_common.Finding(
                path=pathlib.Path(path),
                message=message,
                severity=python_tool_common.Severity.WARN,
                tool="pylint",
                rule_id=rule_id,
                line=int(line),
                column=int(column),
            )
        )

    aspect_arguments.tool_output.write_text(str(findings))
    if findings:
        logging.info("Created pylint output at: %s", aspect_arguments.tool_output)
        raise python_tool_common.LinterFindingAsError(findings=findings)


def main():
    """Interfaces python tool aspect and use pylint to check a given set of files."""

    args = python_tool_common.parse_args()

    logging.basicConfig(level=logging.DEBUG)

    check_with_pylint(aspect_arguments=args)


if __name__ == "__main__":  # pragma: no cover
    main()

"""A runner that interfaces python tool aspect and runs mypy on a list of files."""

import logging
import os
import pathlib

from quality.private.python.tools import python_tool_common

MYPY_BAD_CHECK_ERROR_CODE = 1


def check_with_mypy(aspect_arguments: python_tool_common.AspectArguments) -> None:
    """Run a mypy subprocess, check its output and write its findings to a file.

    :param aspect_arguments:
        The arguments received from the python_tool_aspect and already processed by
         python_tool_common module.
    :raises LinterFindingAsError:
        If mypy finds a file to be formatted.
    """

    pylint_env = os.environ
    findings = python_tool_common.Findings()
    for target_import in aspect_arguments.target_imports | aspect_arguments.target_dependencies:
        if "PYTHONPATH" not in pylint_env:
            pylint_env["PYTHONPATH"] = str(target_import)
        else:
            pylint_env["PYTHONPATH"] += ":" + str(target_import)

    try:
        mypy_output = python_tool_common.execute_subprocess(
            [
                f"{aspect_arguments.tool}",
                "--config-file",
                f"{aspect_arguments.tool_config}",
                "--show-column-numbers",
                *map(str, aspect_arguments.target_files),
            ],
        )
    except python_tool_common.LinterSubprocessError as exception:
        if exception.return_code != MYPY_BAD_CHECK_ERROR_CODE:
            raise exception

        mypy_output = python_tool_common.SubprocessInfo(
            exception.stdout,
            exception.stderr,
            exception.return_code,
        )

    # The last line of mypy's stdout does not contain any finding. Instead, it
    #  contains information about how many files are ok and how many are have issues.
    issues = mypy_output.stdout.splitlines()[:-1]

    for issue in issues:
        path, line, column, _, message_and_rule = issue.split(":", 4)
        message, rule_id = message_and_rule.rsplit(" ", 1)
        findings.append(
            python_tool_common.Finding(
                path=pathlib.Path(path),
                message=message.strip(),
                severity=python_tool_common.Severity.WARN,
                tool="mypy",
                rule_id=rule_id.strip("[]"),
                line=int(line),
                column=int(column),
            )
        )

    aspect_arguments.tool_output.write_text(str(findings))

    if findings:
        logging.info("Created mypy output at: %s", aspect_arguments.tool_output)
        raise python_tool_common.LinterFindingAsError(findings=findings)


def main():
    """Interfaces python tool aspect and use mypy to check a given set of files."""

    args = python_tool_common.parse_args()

    logging.basicConfig(level=logging.DEBUG)

    check_with_mypy(aspect_arguments=args)


if __name__ == "__main__":
    main()

"""A runner that interfaces python tool aspect and runs isort on a list of files."""

import logging
import pathlib

from quality.private.python.tools import python_tool_common

ISORT_BAD_CHECK_ERROR_CODE = 1
ISORT_ERROR_MSG = "ERROR: "


def check_with_isort(aspect_arguments: python_tool_common.AspectArguments) -> None:
    """Run a isort subprocess, check its output and write its findings to a file.

    :param aspect_arguments:
        The arguments received from the python_tool_aspect and already processed by
         python_tool_common module.
    :raises LinterFindingAsError:
        If isort finds a file to be formatted.
    """
    findings = python_tool_common.Findings()

    try:
        isort_output = python_tool_common.execute_subprocess(
            [
                f"{aspect_arguments.tool}",
                "--check-only",
                "--diff",
                "--sp",
                f"{aspect_arguments.tool_config}",
                "--src",
                f"{pathlib.Path.cwd()}",
                "--",
                *map(str, aspect_arguments.target_files),
            ],
        )
    except python_tool_common.LinterSubprocessError as exception:
        if exception.return_code != ISORT_BAD_CHECK_ERROR_CODE:
            raise exception

        isort_output = python_tool_common.SubprocessInfo(
            exception.stdout,
            exception.stderr,
            exception.return_code,
        )

    for line in isort_output.stderr.splitlines():
        file = line.lstrip(ISORT_ERROR_MSG).split(" ")[0]
        findings.append(
            python_tool_common.Finding(
                path=pathlib.Path(file),
                message="Imports are incorrectly sorted and/or formatted.",
                severity=python_tool_common.Severity.WARN,
                tool="isort",
                rule_id="imports_formatting",
            )
        )

    aspect_arguments.tool_output.write_text(str(findings))
    if findings:
        logging.info("Created isort output at: %s", aspect_arguments.tool_output)
        raise python_tool_common.LinterFindingAsError(findings=findings)


def main():
    """Interfaces python tool aspect and use isort to check a given set of files."""

    args = python_tool_common.parse_args()

    logging.basicConfig(level=logging.DEBUG)

    check_with_isort(aspect_arguments=args)


if __name__ == "__main__":  # pragma: no cover
    main()

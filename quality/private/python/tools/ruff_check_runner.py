"""A runner that interfaces python tool aspect and runs ruff on a list of files."""

import json
import logging

from quality.private.python.tools import python_tool_common

RUFF_BAD_CHECK_ERROR_CODE = 1


def check_with_ruff(aspect_arguments: python_tool_common.AspectArguments) -> None:
    """Run a ruff check subprocess, check its output and write its findings to a file.

    :param aspect_arguments:
        The arguments received from the python_tool_aspect and already processed by
         python_tool_common module.
    :raises LinterFindingAsError:
        If ruff finds a file to be formatted.
    :exit codes:
    0 if no violations were found, or if all present violations were fixed
    automatically.
    1 if violations were found.
    2 if Ruff terminates abnormally due to invalid configuration, invalid CLI options,
    or an internal error.
    """
    findings = python_tool_common.Findings()

    try:
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

        python_tool_common.execute_subprocess(subprocess_list)
    except python_tool_common.LinterSubprocessError as exception:
        if exception.return_code != RUFF_BAD_CHECK_ERROR_CODE:
            raise exception

        for finding in json.loads(exception.stdout):
            findings.append(
                python_tool_common.Finding(
                    path=finding["filename"],
                    message=finding["message"],
                    severity=python_tool_common.Severity.WARN,
                    tool="ruff_check",
                    rule_id=finding["code"],
                    line=finding["location"]["row"],
                    column=finding["location"]["column"],
                )
            )

    aspect_arguments.tool_output.write_text(str(findings))
    if findings:
        logging.info("Created ruff check output at: %s", aspect_arguments.tool_output)
        raise python_tool_common.LinterFindingAsError(findings=findings)


def main():
    """Interfaces python tool aspect and use ruff to check a given set of files."""

    args = python_tool_common.parse_args()

    logging.basicConfig(level=logging.DEBUG)

    check_with_ruff(aspect_arguments=args)


if __name__ == "__main__":
    main()

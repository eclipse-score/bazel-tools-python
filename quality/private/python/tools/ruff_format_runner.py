"""A runner that interfaces python tool aspect and runs ruff on a list of files."""

import logging
import pathlib

from quality.private.python.tools import python_tool_common

RUFF_BAD_CHECK_ERROR_CODE = 1


def format_with_ruff(aspect_arguments: python_tool_common.AspectArguments) -> None:
    """Run a ruff format subprocess, check its output and write its findings to a file.

    :param aspect_arguments:
        The arguments received from the python_tool_aspect and already processed by
         python_tool_common module.
    :raises LinterFindingAsError:
        If ruff finds a file to be formatted.
    :exit codes:
    0 if Ruff terminates successfully, and no files would be formatted if --check
    were not specified.
    1 if Ruff terminates successfully, and one or more files would be formatted if
    --check were not specified.
    2 if Ruff terminates abnormally due to invalid configuration, invalid CLI options,
    or an internal error.
    """
    findings = python_tool_common.Findings()

    try:
        subprocess_list = [
            f"{aspect_arguments.tool}",
            "format",
            "--config",
            f"{aspect_arguments.tool_config}",
            *map(str, aspect_arguments.target_files),
        ]
        if not aspect_arguments.refactor:
            subprocess_list[4:4] = ["--diff"]

        ruff_output = python_tool_common.execute_subprocess(subprocess_list)
    except python_tool_common.LinterSubprocessError as exception:
        if exception.return_code != RUFF_BAD_CHECK_ERROR_CODE:
            raise exception

        ruff_output = python_tool_common.SubprocessInfo(
            exception.stdout,
            exception.stderr,
            exception.return_code,
        )

        files = {file.lstrip("-").strip() for file in ruff_output.stdout.splitlines() if file.startswith("---")}

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

    aspect_arguments.tool_output.write_text(str(findings))
    if findings:
        logging.info("Created ruff format output at: %s", aspect_arguments.tool_output)
        raise python_tool_common.LinterFindingAsError(findings=findings)


def main():
    """Interfaces python tool aspect and use ruff to check a given set of files."""

    args = python_tool_common.parse_args()

    logging.basicConfig(level=logging.DEBUG)

    format_with_ruff(aspect_arguments=args)


if __name__ == "__main__":
    main()

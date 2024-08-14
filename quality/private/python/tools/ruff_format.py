"""A runner that interfaces python tool aspect and runs ruff on a list of files."""

import logging

from quality.private.python.tools import python_tool_common

RUFF_BAD_CHECK_ERROR_CODE = 1


def format_with_ruff(aspect_arguments: python_tool_common.AspectArguments) -> None:
    """Run a ruff format subprocess, check its output and write its findings to a file.

    :param aspect_arguments:
        The arguments received from the python_tool_aspect and already processed by
         python_tool_common module.
    :raises LinterFindingAsError:
        If ruff finds a file to be formatted.
    """

    try:
        ruff_output = python_tool_common.execute_subprocess(
            [
                f"{aspect_arguments.tool}",
                "format",
                "--config",
                f"{aspect_arguments.tool_config}",
                "--diff",
                *map(str, aspect_arguments.target_files),
            ],
        )
    except python_tool_common.LinterSubprocessError as exception:
        if exception.return_code != RUFF_BAD_CHECK_ERROR_CODE:
            raise
        ruff_output = python_tool_common.SubprocessInfo(
            exception.stdout,
            exception.stderr,
            exception.return_code,
        )

    aspect_arguments.tool_output.write_text(ruff_output.stdout)
    logging.info("Created ruff output at: %s", aspect_arguments.tool_output)

    if ruff_output.return_code:
        raise python_tool_common.LinterFindingAsError(
            path=aspect_arguments.tool_output,
            tool=aspect_arguments.tool.name,
        )


def main():
    """Interfaces python tool aspect and use ruff to check a given set of files."""

    args = python_tool_common.parse_args()

    logging.basicConfig(level=logging.DEBUG)

    format_with_ruff(aspect_arguments=args)


if __name__ == "__main__":
    main()

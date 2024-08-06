"""A runner that interfaces python tool aspect and runs isort on a list of files."""

import logging

from quality.private.python.tools import python_tool_common

ISORT_BAD_CHECK_ERROR_CODE = 1


def check_with_isort(aspect_arguments: python_tool_common.AspectArguments) -> None:
    """Run a isort subprocess, check its output and write its findings to a file.

    :param aspect_arguments:
        The arguments received from the python_tool_aspect and already processed by
         python_tool_common module.
    :raises LinterFindingAsError:
        If isort finds a file to be formatted.
    """

    try:
        isort_output = python_tool_common.execute_subprocess(
            [
                f"{aspect_arguments.tool}",
                "--check-only",
                "--diff",
                "--sp",
                f"{aspect_arguments.tool_config}",
                "--",
                *map(str, aspect_arguments.target_files),
            ],
        )
    except python_tool_common.LinterSubprocessError as exception:
        if exception.return_code != ISORT_BAD_CHECK_ERROR_CODE:
            raise
        isort_output = python_tool_common.SubprocessInfo(
            exception.stdout,
            exception.stderr,
            exception.return_code,
        )

    aspect_arguments.tool_output.write_text(isort_output.stdout)
    logging.info("Created isort output at: %s", aspect_arguments.tool_output)

    if isort_output.return_code:
        raise python_tool_common.LinterFindingAsError(
            path=aspect_arguments.tool_output,
            tool=aspect_arguments.tool.name,
        )


def main():
    """Interfaces python tool aspect and use isort to check a given set of files."""

    args = python_tool_common.parse_args()

    logging.basicConfig(level=logging.DEBUG)

    check_with_isort(aspect_arguments=args)


if __name__ == "__main__":
    main()

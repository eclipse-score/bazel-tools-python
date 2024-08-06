"""A runner that interfaces python tool aspect and runs black on a list of files."""

import logging

from quality.private.python.tools import python_tool_common

BLACK_DEFAULT_ERROR_MSG = "file would be reformatted"


def check_with_black(aspect_arguments: python_tool_common.AspectArguments) -> None:
    """Run a black subprocess, check its output and write its findings to a file.

    :param aspect_arguments:
        The arguments received from the python_tool_aspect and already processed by
         python_tool_common module.
    :raises LinterFindingAsError:
        If black finds a file to be formatted.
    """

    black_output = python_tool_common.execute_subprocess(
        [
            f"{aspect_arguments.tool}",
            "--diff",
            "--config",
            f"{aspect_arguments.tool_config}",
            *map(str, aspect_arguments.target_files),
        ],
    )

    aspect_arguments.tool_output.write_text(black_output.stdout)
    logging.info("Created black output at: %s", aspect_arguments.tool_output)

    if BLACK_DEFAULT_ERROR_MSG in black_output.stderr:
        raise python_tool_common.LinterFindingAsError(
            path=aspect_arguments.tool_output,
            tool=aspect_arguments.tool.name,
        )


def main():
    """Interfaces python tool aspect and use black to check a given set of files."""

    args = python_tool_common.parse_args()

    logging.basicConfig(level=logging.DEBUG)

    check_with_black(aspect_arguments=args)


if __name__ == "__main__":
    main()

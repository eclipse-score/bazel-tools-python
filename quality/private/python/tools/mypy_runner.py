"""A runner that interfaces python tool aspect and runs mypy on a list of files."""

import logging
import os

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
                *map(str, aspect_arguments.target_files),
            ],
        )
    except python_tool_common.LinterSubprocessError as exception:
        if exception.return_code != MYPY_BAD_CHECK_ERROR_CODE:
            raise
        mypy_output = python_tool_common.SubprocessInfo(
            exception.stdout,
            exception.stderr,
            exception.return_code,
        )

    aspect_arguments.tool_output.write_text(mypy_output.stdout)
    logging.info("Created mypy output at: %s", aspect_arguments.tool_output)

    if mypy_output.return_code:
        raise python_tool_common.DeprecatedLinterFindingAsError(
            path=aspect_arguments.tool_output,
            tool=aspect_arguments.tool.name,
        )


def main():
    """Interfaces python tool aspect and use mypy to check a given set of files."""

    args = python_tool_common.parse_args()

    logging.basicConfig(level=logging.DEBUG)

    check_with_mypy(aspect_arguments=args)


if __name__ == "__main__":
    main()

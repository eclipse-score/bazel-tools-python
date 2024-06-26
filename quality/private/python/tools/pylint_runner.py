"""A runner that interfaces python tool aspect and runs pylint on a list of files."""

import logging
import os

from quality.private.python.tools import python_tool_common


def check_with_pylint(aspect_arguments: python_tool_common.AspectArguments) -> None:
    """Run a pylint subprocess, check its output and write its findings to a file."""

    pylint_env = os.environ
    for target_import in aspect_arguments.target_imports | aspect_arguments.target_dependencies:
        if "PYTHONPATH" not in pylint_env:
            pylint_env["PYTHONPATH"] = str(target_import)
        else:
            pylint_env["PYTHONPATH"] += ":" + str(target_import)

    try:
        python_tool_common.execute_subprocess(
            [
                # Binary executable path.
                f"{aspect_arguments.tool}",
                # Configuration flag and path.
                "--rcfile",
                f"{aspect_arguments.tool_config}",
                # Putput a colorized text to a given path.
                f"--output-format=text:{aspect_arguments.tool_output},colorized",
                # Text content template.
                "--msg-template",
                "{path}:{line}:{column}: {msg} [{msg_id}, {symbol}]",
                # Exclude pylint persistent output as this would be both action input and output.
                "--persistent",
                "no",
                # Files to lint
                "--",
                *aspect_arguments.target_files,
            ],
            env=pylint_env,
        )
    finally:
        logging.info("Created pylint output at: %s", aspect_arguments.tool_output)


def main():
    """Interfaces python tool aspect and use pylint to check a given set of files."""

    args = python_tool_common.parse_args()

    logging.basicConfig(level=logging.DEBUG)

    check_with_pylint(aspect_arguments=args)


if __name__ == "__main__":
    main()

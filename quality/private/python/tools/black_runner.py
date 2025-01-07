"""A runner that interfaces python tool aspect and runs black on a list of files."""

import logging
import pathlib

from quality.private.python.tools import python_tool_common

WOULD_REFORMAT_MSG = "would reformat"


def _removeprefix(text: str, prefix: str) -> str:
    """Remove a certain prefix from a a given text.

    This function is supposed to add backwards compartibility with python 3.8 as
    python versions equal or greater than 3.9 already offer this as a built in.
    """
    if text.startswith(prefix):
        return text[len(prefix) :].strip()
    return text


def check_with_black(aspect_arguments: python_tool_common.AspectArguments) -> None:
    """Run a black subprocess, check its output and write its findings to a file.

    :param aspect_arguments:
        The arguments received from the python_tool_aspect and already processed by
        python_tool_common module.
    :raises LinterFindingAsError:
        If black finds at least one file to be formatted.
    """

    findings = python_tool_common.Findings()

    subprocess_list = [
        f"{aspect_arguments.tool}",
        "--diff",
        "--config",
        f"{aspect_arguments.tool_config}",
        *map(str, aspect_arguments.target_files),
    ]
    if aspect_arguments.refactor:
        subprocess_list.remove("--diff")

    black_output = python_tool_common.execute_subprocess(subprocess_list)

    for line in black_output.stderr.splitlines():
        if line.startswith(WOULD_REFORMAT_MSG):
            file = _removeprefix(line, WOULD_REFORMAT_MSG)
            findings += [
                python_tool_common.Finding(
                    path=pathlib.Path(file),
                    message="Should be reformatted.",
                    severity=python_tool_common.Severity.WARN,
                    tool="black",
                    rule_id="formatting",
                )
            ]

    aspect_arguments.tool_output.write_text(str(findings))
    if findings:
        logging.info("Created black output at: %s", aspect_arguments.tool_output)
        raise python_tool_common.LinterFindingAsError(findings=findings)


def main():
    """Interfaces python tool aspect and use black to check a given set of files."""

    args = python_tool_common.parse_args()

    logging.basicConfig(level=logging.DEBUG)

    check_with_black(aspect_arguments=args)


if __name__ == "__main__":  # pragma: no cover
    main()

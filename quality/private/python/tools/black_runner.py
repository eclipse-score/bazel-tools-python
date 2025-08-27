# *******************************************************************************
# Copyright (c) 2025 Contributors to the Eclipse Foundation
#
# See the NOTICE file(s) distributed with this work for additional
# information regarding copyright ownership.
#
# This program and the accompanying materials are made available under the
# terms of the Apache License Version 2.0 which is available at
# https://www.apache.org/licenses/LICENSE-2.0
#
# SPDX-License-Identifier: Apache-2.0
# *******************************************************************************
"""A runner that interfaces python tool aspect and runs black on a list of files."""

import pathlib
import typing as t

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


def get_black_command(aspect_arguments: python_tool_common.AspectArguments) -> t.List[str]:
    """Returns the command to run a black subprocess."""

    subprocess_list = [
        f"{aspect_arguments.tool}",
        "--diff",
        "--config",
        f"{aspect_arguments.tool_config}",
        *map(str, aspect_arguments.target_files),
    ]
    if aspect_arguments.refactor:
        subprocess_list.remove("--diff")

    return subprocess_list


def black_output_parser(tool_output: python_tool_common.SubprocessInfo) -> python_tool_common.Findings:
    """Parses `tool_output` to get the findings returned from the tool execution."""

    findings = python_tool_common.Findings()

    for line in tool_output.stderr.splitlines():
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

    return findings


def main():
    """Main entry point."""
    python_tool_common.execute_runner(
        get_command=get_black_command,
        output_parser=black_output_parser,
    )


if __name__ == "__main__":  # pragma: no cover
    main()

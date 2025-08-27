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
"""A runner that interfaces python tool aspect and runs isort on a list of files."""

import pathlib
import typing as t

from quality.private.python.tools import python_tool_common

ISORT_BAD_CHECK_ERROR_CODE = 1
ISORT_ERROR_MSG = "ERROR: "


def get_isort_command(aspect_arguments: python_tool_common.AspectArguments) -> t.List[str]:
    """Returns the command to run an isort subprocess."""
    subprocess_list = [
        f"{aspect_arguments.tool}",
        "--sp",
        f"{aspect_arguments.tool_config}",
        "--src",
        f"{pathlib.Path.cwd()}",
        "--",
        *map(str, aspect_arguments.target_files),
    ]

    if not aspect_arguments.refactor:
        subprocess_list[1:1] = ["--check-only", "--diff"]

    return subprocess_list


def isort_output_parser(tool_output: python_tool_common.SubprocessInfo) -> python_tool_common.Findings:
    """Parses `tool_output` to get the findings returned from the tool execution."""
    findings = python_tool_common.Findings()

    for line in tool_output.stderr.splitlines():
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

    return findings


def isort_exception_handler(exception: python_tool_common.LinterSubprocessError) -> python_tool_common.SubprocessInfo:
    """Handles the cases that isort has a non-zero return code."""
    if exception.return_code != ISORT_BAD_CHECK_ERROR_CODE:
        raise exception

    return python_tool_common.SubprocessInfo(
        exception.stdout,
        exception.stderr,
        exception.return_code,
    )


def main():
    """Main entry point."""
    python_tool_common.execute_runner(
        get_command=get_isort_command,
        output_parser=isort_output_parser,
        exception_handler=isort_exception_handler,
    )


if __name__ == "__main__":  # pragma: no cover
    main()

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
"""A runner that interfaces python tool aspect and runs pylint on a list of files."""

import pathlib
import typing as t

from quality.private.python.tools import python_tool_common

PYLINT_MODULE_START_MSG = "************* Module"


def is_pylint_critical_error(exception: python_tool_common.LinterSubprocessError) -> bool:
    """Checks if the return code represents a pylint critical error.

    Cases considered:
    - Pylint returns an odd number when a fatal error occurs;
    - Pylint returns 32 when an unrecognized option is used in the CLI call;
    - Pylint returns an error message in stderr when an option is configured with a invalid value.
    """
    return_code = int(exception.return_code)
    return (return_code % 2) == 1 or return_code == 32 or exception.stderr != ""


def get_pylint_command(aspect_arguments: python_tool_common.AspectArguments) -> t.List[str]:
    """Returns the command to run a pylint subprocess."""

    return [
        # Binary executable path.
        f"{aspect_arguments.tool}",
        # Configuration flag and path.
        "--rcfile",
        f"{aspect_arguments.tool_config}",
        # Text content template.
        "--msg-template",
        "{path}:{line}:{column}:{msg}:{symbol}",
        # Exclude pylint persistent output as this would be both action input and output.
        "--persistent",
        "no",
        "--score",
        "no",
        # Files to lint
        "--",
        *map(str, aspect_arguments.target_files),
    ]


def pylint_output_parser(tool_output: python_tool_common.SubprocessInfo) -> python_tool_common.Findings:
    """Parses `tool_output` to get the findings returned from the tool execution."""

    findings = python_tool_common.Findings()

    for output_line in tool_output.stdout.splitlines():
        if output_line.startswith(PYLINT_MODULE_START_MSG):
            continue

        path, line, column, message, rule_id = output_line.rsplit(":", 4)

        findings.append(
            python_tool_common.Finding(
                path=pathlib.Path(path),
                message=message,
                severity=python_tool_common.Severity.WARN,
                tool="pylint",
                rule_id=rule_id,
                line=int(line),
                column=int(column),
            )
        )

    return findings


def pylint_exception_handler(exception: python_tool_common.LinterSubprocessError) -> python_tool_common.SubprocessInfo:
    """Handles the cases that pylint has a non-zero return code."""
    if is_pylint_critical_error(exception):
        raise exception

    return python_tool_common.SubprocessInfo(
        exception.stdout,
        exception.stderr,
        exception.return_code,
    )


def main():
    """Main entry point."""
    python_tool_common.execute_runner(
        get_command=get_pylint_command,
        output_parser=pylint_output_parser,
        exception_handler=pylint_exception_handler,
    )


if __name__ == "__main__":  # pragma: no cover
    main()

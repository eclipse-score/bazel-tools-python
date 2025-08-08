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
"""A runner that interfaces python tool aspect and runs mypy on a list of files."""

import pathlib
import typing as t

from quality.private.python.tools import python_tool_common

MYPY_BAD_CHECK_ERROR_CODE = 1


def get_mypy_command(aspect_arguments: python_tool_common.AspectArguments) -> t.List[str]:
    """Returns the command to run mypy on a subprocess."""
    return [
        f"{aspect_arguments.tool}",
        "--config-file",
        f"{aspect_arguments.tool_config}",
        "--show-column-numbers",
        *map(str, aspect_arguments.target_files),
    ]


def mypy_output_parser(tool_output: python_tool_common.SubprocessInfo) -> python_tool_common.Findings:
    """Parses `tool_output` to get the findings returned from the tool execution."""

    findings = python_tool_common.Findings()
    issues = tool_output.stdout.splitlines()[:-1]

    for issue in issues:
        path, line, column, _, message_and_rule = issue.split(":", 4)
        message, rule_id = message_and_rule.rsplit(" ", 1)
        findings.append(
            python_tool_common.Finding(
                path=pathlib.Path(path),
                message=message.strip(),
                severity=python_tool_common.Severity.WARN,
                tool="mypy",
                rule_id=rule_id.strip("[]"),
                line=int(line),
                column=int(column),
            )
        )

    return findings


def mypy_exception_handler(exception: python_tool_common.LinterSubprocessError) -> python_tool_common.SubprocessInfo:
    """Handles the cases that mypy has a non-zero return code."""
    if exception.return_code != MYPY_BAD_CHECK_ERROR_CODE:
        raise exception

    return python_tool_common.SubprocessInfo(
        exception.stdout,
        exception.stderr,
        exception.return_code,
    )


def main():
    """Main entry point."""
    python_tool_common.execute_runner(
        get_command=get_mypy_command,
        output_parser=mypy_output_parser,
        exception_handler=mypy_exception_handler,
    )


if __name__ == "__main__":  # pragma: no cover
    main()

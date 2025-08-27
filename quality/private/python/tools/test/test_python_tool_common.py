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
"""Tests for the python tool common."""

import filecmp
import json
import os
import subprocess
from pathlib import Path

import pytest
from pytest_mock import MockerFixture

from quality.private.python.tools import python_tool_common


def test_findings_to_json_file_and_to_text_file(tmp_path: Path) -> None:
    """Test Findings to_json_file and to_text_file methods"""

    dummy_finding = python_tool_common.Finding(
        path=Path("file.py"),
        message="Generic error message",
        severity=python_tool_common.Severity.WARN,
        tool="tool",
        rule_id="generic",
        line=1,
        column=1,
    )
    findings = python_tool_common.Findings([dummy_finding])
    expected_message = "file.py:1:1: Generic error message [tool:generic]"
    expected_findings = [
        {
            "path": "file.py",
            "message": "Generic error message",
            "severity": "WARN",
            "tool": "tool",
            "rule_id": "generic",
            "line": 1,
            "column": 1,
        }
    ]
    output_text_file_path = tmp_path / "findings.text"
    output_json_file_path = tmp_path / "findings.json"
    findings.to_text_file(file=output_text_file_path)
    findings.to_json_file(file=output_json_file_path)

    text_findings = output_text_file_path.read_text()
    json_findings = json.loads(output_json_file_path.read_text())

    assert expected_message == str(dummy_finding)
    assert text_findings == expected_message
    assert json_findings == expected_findings


@pytest.mark.parametrize(
    "stdout, expected_findings",
    [
        (
            "",
            python_tool_common.Findings([]),
        ),
        (
            "file.py,Imports are incorrectly sorted and/or formatted.,WARN,generic_tool,[imports_formatting],2,3",
            python_tool_common.Findings(
                [
                    python_tool_common.Finding(
                        path=Path("file.py"),
                        message="Imports are incorrectly sorted and/or formatted.",
                        severity=python_tool_common.Severity.WARN,
                        tool="generic_tool",
                        rule_id="[imports_formatting]",
                        line=2,
                        column=3,
                    )
                ]
            ),
        ),
    ],
)
def test_successful_execute_runner(
    mocker: MockerFixture,
    stdout: str,
    expected_findings: python_tool_common.Findings,
    aspect_args: python_tool_common.AspectArguments,
    tmp_path: Path,
) -> None:
    """Test execute runner function with and without findings.

    Since this test will use all available tools, it's natural that the function
    call will have too many arguments and local arguments.
    """
    aspect_args.tool_root = "_main"
    subprocess_info = python_tool_common.SubprocessInfo(
        stdout=stdout,
        stderr="",
        return_code=0,
    )
    mocker.patch(
        "quality.private.python.tools.python_tool_common.execute_subprocess",
        return_value=subprocess_info,
    )
    mocker.patch(
        "quality.private.python.tools.python_tool_common.parse_args",
        return_value=aspect_args,
    )
    text_file = tmp_path / "finding.text"
    expected_findings.to_text_file(text_file)
    json_file = tmp_path / "finding.json"
    expected_findings.to_json_file(json_file)
    output_parser = mocker.MagicMock(return_value=expected_findings)

    if subprocess_info.stdout == "":
        python_tool_common.execute_runner(
            get_command=lambda _: [""],
            output_parser=output_parser,
        )
    else:
        with pytest.raises(python_tool_common.LinterFindingAsError):
            python_tool_common.execute_runner(
                get_command=lambda _: [""],
                output_parser=output_parser,
            )

    output_parser.assert_called_with(subprocess_info)
    assert filecmp.cmp(text_file, aspect_args.tool_output_text)
    assert filecmp.cmp(json_file, aspect_args.tool_output_json)


def test_execute_runner_fault_without_exception_handler(
    mocker: MockerFixture,
    aspect_args: python_tool_common.AspectArguments,
):
    """Test execute runner function with exceptions but without exception handler."""
    mocker.patch(
        "quality.private.python.tools.python_tool_common.execute_subprocess",
        side_effect=[
            python_tool_common.LinterSubprocessError(
                commands=["tool"],
                return_code=1,
                stdout="exception.stdout",
                stderr="exception.stderr",
            )
        ],
    )
    mocker.patch(
        "quality.private.python.tools.python_tool_common.parse_args",
        return_value=aspect_args,
    )
    expected_error = python_tool_common.LinterSubprocessError

    with pytest.raises(expected_error):
        python_tool_common.execute_runner(
            get_command=lambda _: [""],
            output_parser=lambda _: python_tool_common.Findings([]),
            exception_handler=None,
        )


def test_execute_runner_fault_with_exception_handler(
    mocker: MockerFixture,
    aspect_args: python_tool_common.AspectArguments,
):
    """Test execute runner function with exceptions and with excpetion handler."""
    mocker.patch(
        "quality.private.python.tools.python_tool_common.execute_subprocess",
        side_effect=[
            python_tool_common.LinterSubprocessError(
                commands=["tool"],
                return_code=1,
                stdout="exception.stdout",
                stderr="exception.stderr",
            )
        ],
    )
    mocker.patch(
        "quality.private.python.tools.python_tool_common.parse_args",
        return_value=aspect_args,
    )
    expected_error = python_tool_common.LinterFindingAsError
    expected_finding = python_tool_common.Finding(
        path=Path("file.py"),
        message="exception.stdout",
        severity=python_tool_common.Severity.WARN,
        tool="tool",
        rule_id="exception",
    )
    exception_handler = mocker.MagicMock(
        return_value=python_tool_common.SubprocessInfo(
            stdout="--- file.py",
            stderr="Tool found an error.\n",
            return_code=1,
        )
    )

    with pytest.raises(expected_error):
        python_tool_common.execute_runner(
            get_command=lambda _: [""],
            output_parser=lambda _: python_tool_common.Findings([expected_finding]),
            exception_handler=exception_handler,
        )


def test_stop_iteration_except_case() -> None:
    """Test if AspectArguments StopIteration excpetion is properly raised.

    The exception will be raised when the path for target_file can't be found."""
    expected_message = "Therefore generic_tool cannot properly run."

    with pytest.raises(python_tool_common.PythonPathNotFoundError) as excpt:
        python_tool_common.AspectArguments(
            target_imports={Path("")},
            target_dependencies={Path("")},
            target_files={Path("wrong_folder/test_file.py")},
            tool=Path("/generic_tool"),
            tool_config=Path(""),
            tool_output_text=Path(""),
            tool_output_json=Path(""),
            tool_root="main",
            refactor=False,
        )

    assert expected_message in str(excpt)


def test_bazel_check_case(
    mocker: MockerFixture, aspect_args: python_tool_common.AspectArguments, tmp_path: Path
) -> None:
    """Test if AspectArguments checks for bazel generated files before raising an except."""
    mocker.patch("builtins.open", side_effect=FileNotFoundError)
    mocker.patch.object(Path, "glob", return_value={Path("path/to/test_python_tool_common.py")})
    tmp_text_file_path = tmp_path / "output.text"
    tmp_json_file_path = tmp_path / "output.json"
    expected_target_file = {Path("path/to/test_python_tool_common.py")}

    aspect_args = python_tool_common.AspectArguments(
        target_imports={Path("")},
        target_dependencies={Path("")},
        target_files={Path("path/to/file.py")},
        tool=Path("path/to/tool_entry_point"),
        tool_config=Path("path/to/pyproject.toml"),
        tool_output_text=tmp_text_file_path,
        tool_output_json=tmp_json_file_path,
        tool_root="_main",
        refactor=False,
    )

    assert aspect_args.target_files == expected_target_file


def test_resolve_relative_paths_valid(mocker: MockerFixture, tmp_path: Path) -> None:
    """Test AspectArguments path resolution when no exception is raised.

    Also tests the enviroment for target_imports.
    """
    mocker.patch.object(Path, "glob", return_value={Path("quality/private/python/ruff_entry_point")})
    mocker.patch.dict(os.environ, {}, clear=True)
    target_imports = {Path("path/to/imports")}
    target_files = {Path("quality/private/python/ruff_entry_point")}
    tool = Path("path/to/tool_entry_point")
    tool_config = Path("path/to/pyproject.toml")
    tmp_text_file_path = tmp_path / "output.text"
    tmp_json_file_path = tmp_path / "output.json"
    expected_tool_path = Path("path/to/tool_entry_point")
    expected_tool_config_path = Path("path/to/pyproject.toml")

    aspect_args = python_tool_common.AspectArguments(
        target_imports=target_imports,
        target_dependencies={Path("")},
        target_files=target_files,
        tool=tool,
        tool_config=tool_config,
        tool_output_text=tmp_text_file_path,
        tool_output_json=tmp_json_file_path,
        tool_root="quality",
        refactor=False,
    )

    assert aspect_args.tool == expected_tool_path
    assert aspect_args.tool_config == expected_tool_config_path
    assert aspect_args.refactor is False


def test_execute_subprocess(mocker: MockerFixture) -> None:
    """Test the execute_subprocess function with a zero return code."""
    mocker.patch(
        "subprocess.run",
        return_value=subprocess.CompletedProcess(
            args=[],
            returncode=0,
            stdout="",
            stderr="exception stdeer",
        ),
    )
    commands = [
        "path/to/tool_entry_point",
        "--diff",
        "--config",
        "path/to/pyproject.toml",
        "path/to/test.py",
    ]
    expected_stderr = "exception stdeer"
    expected_return_code = 0

    info = python_tool_common.execute_subprocess(commands=commands)

    assert info.stdout == ""
    assert info.stderr == expected_stderr
    assert info.return_code == expected_return_code


def test_execute_subprocess_error(mocker: MockerFixture) -> None:
    """Test the execute_subprocess function raising LinterSubprocessError."""
    commands = ["false"]
    mocker.patch(
        "subprocess.run",
        side_effect=subprocess.CalledProcessError(
            cmd=commands,
            returncode=1,
            output="An error ocurred.",
        ),
    )
    expected_output = f'The command "{commands}" returned code "1" and the following error message:\nAn error ocurred.'

    with pytest.raises(python_tool_common.LinterSubprocessError) as excpt:
        python_tool_common.execute_subprocess(commands=commands)

    assert str(excpt.value) == expected_output

"""pytest fixtures for the config-generator test"""

import pathlib

import pytest

from quality.private.python.tools import python_tool_common


@pytest.fixture(name="subprocess_output", scope="module")
def fixture_subprocess_info(request) -> python_tool_common.SubprocessInfo:
    """Fixture to return a python tool common SubprocessInfo class without errors."""
    stdout, stderr, return_code = request.param

    return python_tool_common.SubprocessInfo(
        stdout=stdout,
        stderr=stderr,
        return_code=return_code,
    )


@pytest.fixture(name="linter_subprocess_error", scope="module")
def fixture_linter_subprocess_error(request) -> python_tool_common.LinterSubprocessError:
    """Fixture to return a generic python tool common LinterSubprocessError."""
    commands, stdout, stderr, return_code = request.param

    return python_tool_common.LinterSubprocessError(
        commands=commands,
        stdout=stdout,
        stderr=stderr,
        return_code=return_code,
    )


@pytest.fixture(name="aspect_args")
def fixture_aspect_argument(tmp_path: pathlib.Path) -> python_tool_common.AspectArguments:
    """Fixture to return a python tool common AspectArguments class."""
    test = tmp_path / "test.py"
    test.write_text("")

    return python_tool_common.AspectArguments(
        target_imports=set(),
        target_dependencies=set(),
        target_files=set([test]),
        tool=pathlib.Path("tool.exec"),
        tool_config=pathlib.Path("tool.config"),
        tool_output_text=pathlib.Path("output.text"),
        tool_output_json=pathlib.Path("output.json"),
        tool_root="",
        refactor=False,
    )


@pytest.fixture(name="finding", scope="module")
def fixture_finding(request) -> python_tool_common.Finding:
    """Fixture to return a generic python tool common Finding class."""
    path, message, severity, tool, rule_id, line, column = request.param

    return python_tool_common.Finding(
        path=path,
        message=message,
        severity=severity,
        tool=tool,
        rule_id=rule_id,
        line=line,
        column=column,
    )

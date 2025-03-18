"""pytest fixtures for the config-generator test"""

import pathlib
import tempfile

import pytest

from quality.private.python.tools import python_tool_common


@pytest.fixture(name="subprocess_output", scope="module")
def fixture_subprocessinfo(request) -> python_tool_common.SubprocessInfo:
    """Fixture to return a python tool common SubprocessInfo class without errors."""
    stdout, stderr, return_code = request.param

    return python_tool_common.SubprocessInfo(
        stdout=stdout,
        stderr=stderr,
        return_code=return_code,
    )


@pytest.fixture(name="linter_subprocess_error", scope="module")
def fixture_linter_subprocesserror(request) -> python_tool_common.LinterSubprocessError:
    """Fixture to return a generic python tool common LinterSubprocessError."""
    commands, stdout, stderr, return_code = request.param

    return python_tool_common.LinterSubprocessError(
        commands=commands,
        stdout=stdout,
        stderr=stderr,
        return_code=return_code,
    )


@pytest.fixture(name="aspect_args")
def fixture_aspect_argument() -> python_tool_common.AspectArguments:
    """Fixture to return a python tool common AspectArguments class."""
    tmp_text_file_path = pathlib.Path(tempfile.mkstemp()[1])
    tmp_json_file_path = pathlib.Path(tempfile.mkstemp()[1])
    target_file = pathlib.Path(tempfile.mkstemp()[1])

    return python_tool_common.AspectArguments(
        target_imports=set(),
        target_dependencies=set(),
        target_files=set([target_file]),
        tool=pathlib.Path("tool.exec"),
        tool_config=pathlib.Path("tool.config"),
        tool_output_text=tmp_text_file_path,
        tool_output_json=tmp_json_file_path,
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

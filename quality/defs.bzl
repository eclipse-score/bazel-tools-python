# Copyright (C) 2025 Bayerische Motoren Werke Aktiengesellschaft (BMW AG). All rights reserved.

"""
Defines all public symbols for this modules to be used by the specific project.
"""

load("@bazel_tools_python//quality/private/python:py_pytest.bzl", _py_pytest = "py_pytest")
load(
    "@bazel_tools_python//quality/private/python:python_pip_audit_rule.bzl",
    _pip_audit_rule = "pip_audit_rule",
)
load(
    "@bazel_tools_python//quality/private/python:python_tool_aspect.bzl",
    _black_aspect = "black_aspect",
    _isort_aspect = "isort_aspect",
    _mypy_aspect = "mypy_aspect",
    _pylint_aspect = "pylint_aspect",
    _python_tool_config = "python_tool_config",
    _ruff_check_aspect = "ruff_check_aspect",
    _ruff_format_aspect = "ruff_format_aspect",
)

python_tool_config = _python_tool_config
py_pytest = _py_pytest

# Pylint only works with workspace.
# The problem is related with rules_python bzlmod support.
# See: https://github.com/bazelbuild/rules_python/issues/1575
pylint_aspect = _pylint_aspect
black_aspect = _black_aspect
isort_aspect = _isort_aspect
mypy_aspect = _mypy_aspect
ruff_check_aspect = _ruff_check_aspect
ruff_format_aspect = _ruff_format_aspect

pip_audit_rule = _pip_audit_rule

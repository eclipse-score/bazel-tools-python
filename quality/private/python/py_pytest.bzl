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
"""Custom py_test rule that is compatible with pytest."""

load("@rules_python//python:defs.bzl", "py_test")

_CONFIG = "@bazel_tools_python//quality:quality_pytest_config"

_RUNNER_LABEL = "@bazel_tools_python//quality/private/python/tools:pytest_runner"
_RUNNER_FILE = "pytest_runner.py"

_BASE_SRCS = []
_BASE_DATA = []
_BASE_DEPS = "@bazel_tools_python//quality/private/python:py_test_deps"

def py_pytest(
        name,
        srcs,
        deps = [],
        data = [],
        env = {},
        *args,
        **kwargs):
    """Produces a custom py_test target that is compatible with pytest.

    Args:
        name: A unique name for this target.
        srcs: The list of source (.py) files that are processed to create the target.
        deps: The list of other libraries to be linked in to the binary target.
        data: Files needed by this rule at runtime.
        env: Specifies additional environment variables to set when the target is executed by bazel run.
        *args: Arguments inherited from py_test rule.
        **kwargs: Keyword arguments inherited from py_test rule.
    """

    if "main" in kwargs:
        fail("Error, this rule automatically creates main file in order to enable pytest usage.")

    srcs = depset(srcs + [common_src for common_src in _BASE_SRCS]).to_list()
    data = depset(data + [_CONFIG] + [common_data for common_data in _BASE_DATA]).to_list()
    deps = depset(deps + [_BASE_DEPS]).to_list()

    env = {key: value for key, value in env.items()}
    env.update({"_PYTEST_CONFIG_FILE": "$(location %s)" % Label(_CONFIG)})
    env.update({"_PYTEST_RUNNER_TARGETS": ",".join(["$(location %s)" % src for src in srcs])})

    py_test(
        name = name,
        srcs = srcs + [_RUNNER_LABEL],
        main = _RUNNER_FILE,
        deps = deps,
        data = data,
        env = env,
        *args,
        **kwargs
    )

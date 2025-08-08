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
load("@bazel_tools_python//quality:defs.bzl", "py_pytest")
load("@bazel_tools_python_pip_hub//:loaders.bzl", "pkg")
load("@rules_python//python:defs.bzl", "py_library")

py_pytest(
    name = "test_isort_runner",
    srcs = ["test_isort_runner.py"],
    deps = ["//quality/private/python/tools:isort"],
)

py_pytest(
    name = "test_pylint_runner",
    srcs = ["test_pylint_runner.py"],
    deps = ["//quality/private/python/tools:pylint"],
)

py_pytest(
    name = "test_black_runner",
    srcs = ["test_black_runner.py"],
    deps = ["//quality/private/python/tools:black"],
)

py_pytest(
    name = "test_mypy_runner",
    srcs = ["test_mypy_runner.py"],
    deps = [
        ":conftest",
        "//quality/private/python/tools:mypy",
    ],
)

py_pytest(
    name = "test_ruff_check_runner",
    srcs = ["test_ruff_check_runner.py"],
    deps = [
        ":conftest",
        "//quality/private/python/tools:ruff_check",
    ],
)

py_pytest(
    name = "test_ruff_format_runner",
    srcs = ["test_ruff_format_runner.py"],
    deps = [
        ":conftest",
        "//quality/private/python/tools:ruff_format",
    ],
)

py_library(
    name = "conftest",
    srcs = ["conftest.py"],
    visibility = ["//visibility:public"],
    deps = [
        "//quality/private/python/tools:python_tool_common",
        pkg("pytest"),
    ],
)

py_pytest(
    name = "test_python_tool_common",
    srcs = ["test_python_tool_common.py"],
    deps = [":conftest"],
)

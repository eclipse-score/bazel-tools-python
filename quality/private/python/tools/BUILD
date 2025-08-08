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
load("@bazel_tools_python_pip_hub//:loaders.bzl", "pkg")
load("@rules_python//python:defs.bzl", "py_binary", "py_library")

py_binary(
    name = "pytest_runner",
    srcs = ["pytest_runner.py"],
    visibility = ["//visibility:public"],
    deps = [pkg("pytest")],
)

py_library(
    name = "python_tool_common",
    srcs = ["python_tool_common.py"],
    visibility = ["//quality/private/python/tools:__subpackages__"],
)

py_binary(
    name = "pylint",
    srcs = ["pylint_runner.py"],
    data = ["@bazel_tools_python//quality/private/python:pylint_entry_point"],
    main = "pylint_runner.py",
    visibility = ["//visibility:public"],
    deps = ["@bazel_tools_python//quality/private/python/tools:python_tool_common"],
)

py_binary(
    name = "black",
    srcs = ["black_runner.py"],
    data = ["@bazel_tools_python//quality/private/python:black_entry_point"],
    main = "black_runner.py",
    visibility = ["//visibility:public"],
    deps = ["@bazel_tools_python//quality/private/python/tools:python_tool_common"],
)

py_binary(
    name = "isort",
    srcs = ["isort_runner.py"],
    data = ["@bazel_tools_python//quality/private/python:isort_entry_point"],
    main = "isort_runner.py",
    visibility = ["//visibility:public"],
    deps = ["@bazel_tools_python//quality/private/python/tools:python_tool_common"],
)

py_binary(
    name = "mypy",
    srcs = ["mypy_runner.py"],
    data = ["@bazel_tools_python//quality/private/python:mypy_entry_point"],
    main = "mypy_runner.py",
    visibility = ["//visibility:public"],
    deps = ["@bazel_tools_python//quality/private/python/tools:python_tool_common"],
)

py_binary(
    name = "ruff_check",
    srcs = ["ruff_check_runner.py"],
    main = "ruff_check_runner.py",
    visibility = ["//visibility:public"],
    deps = [
        "@bazel_tools_python//quality/private/python:ruff_entry_point",
        "@bazel_tools_python//quality/private/python/tools:python_tool_common",
    ],
)

py_binary(
    name = "ruff_format",
    srcs = ["ruff_format_runner.py"],
    main = "ruff_format_runner.py",
    visibility = ["//visibility:public"],
    deps = [
        "@bazel_tools_python//quality/private/python:ruff_entry_point",
        "@bazel_tools_python//quality/private/python/tools:python_tool_common",
    ],
)

filegroup(
    name = "pip_audit_runner_template",
    srcs = ["pip_audit_runner.sh.template"],
    visibility = ["//visibility:public"],
)

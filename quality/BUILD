# Copyright 2022 The BMW Group Authors. All rights reserved.

load("@bazel_tools_python//quality:defs.bzl", "python_tool_config")

python_tool_config(
    name = "quality_python_default_config",
    config = "@bazel_tools_python//quality/private/python/support:pyproject_toml",
    visibility = ["//visibility:public"],
)

label_flag(
    name = "quality_pytest_config",
    build_setting_default = "@bazel_tools_python//quality:quality_python_default_config",
    visibility = ["//visibility:public"],
)

label_flag(
    name = "quality_pylint_config",
    build_setting_default = "@bazel_tools_python//quality:quality_python_default_config",
    visibility = ["//visibility:public"],
)

label_flag(
    name = "quality_black_config",
    build_setting_default = "@bazel_tools_python//quality:quality_python_default_config",
    visibility = ["//visibility:public"],
)

label_flag(
    name = "quality_isort_config",
    build_setting_default = "@bazel_tools_python//quality:quality_python_default_config",
    visibility = ["//visibility:public"],
)

label_flag(
    name = "quality_mypy_config",
    build_setting_default = "@bazel_tools_python//quality:quality_python_default_config",
    visibility = ["//visibility:public"],
)

label_flag(
    name = "quality_ruff_config",
    build_setting_default = "@bazel_tools_python//quality:quality_python_default_config",
    visibility = ["//visibility:public"],
)

alias(
    name = "pylint",
    actual = "//quality/private/python:pylint_entry_point",
)

alias(
    name = "black",
    actual = "//quality/private/python:black_entry_point",
)

alias(
    name = "isort",
    actual = "//quality/private/python:isort_entry_point",
)

alias(
    name = "mypy",
    actual = "//quality/private/python:mypy_entry_point",
)

alias(
    name = "ruff",
    actual = "//quality/private/python:ruff_entry_point",
)

alias(
    name = "pip_audit",
    actual = "//quality/private/python:pip_audit_entry_point",
)

alias(
    name = "pycoverage",
    actual = "//quality/private/python:pycoverage_entry_point",
)

load("@swf_bazel_rules_quality_python//:defs.bzl", "py_binary")
load("@swf_bazel_rules_quality_rules_python//python:defs.bzl", "py_library")

py_library(
    name = "python_tool_common",
    srcs = ["python_tool_common.py"],
)

py_binary(
    name = "pylint",
    srcs = ["pylint.py"],
    data = ["@swf_bazel_rules_quality//quality/private/python:pylint_entry_point"],
    visibility = ["//visibility:public"],
    deps = ["@swf_bazel_rules_quality//quality/private/python/tools:python_tool_common"],
)

py_binary(
    name = "black",
    srcs = ["black.py"],
    data = ["@swf_bazel_rules_quality//quality/private/python:black_entry_point"],
    visibility = ["//visibility:public"],
    deps = ["@swf_bazel_rules_quality//quality/private/python/tools:python_tool_common"],
)

py_binary(
    name = "isort",
    srcs = ["isort.py"],
    data = ["@swf_bazel_rules_quality//quality/private/python:isort_entry_point"],
    visibility = ["//visibility:public"],
    deps = ["@swf_bazel_rules_quality//quality/private/python/tools:python_tool_common"],
)

py_binary(
    name = "mypy_runner",
    srcs = ["mypy_runner.py"],
    data = ["@swf_bazel_rules_quality//quality/private/python:mypy"],
    visibility = ["//visibility:public"],
    deps = ["@swf_bazel_rules_quality//quality/private/python/tools:python_tool_common"],
)

py_binary(
    name = "ruff_check",
    srcs = ["ruff_check.py"],
    visibility = ["//visibility:public"],
    deps = [
        "@swf_bazel_rules_quality//quality/private/python:ruff_entry_point",
        "@swf_bazel_rules_quality//quality/private/python/tools:python_tool_common",
    ],
)

py_binary(
    name = "ruff_format",
    srcs = ["ruff_format.py"],
    visibility = ["//visibility:public"],
    deps = [
        "@swf_bazel_rules_quality//quality/private/python:ruff_entry_point",
        "@swf_bazel_rules_quality//quality/private/python/tools:python_tool_common",
    ],
)

load("@swf_bazel_rules_quality_python//:defs.bzl", "py_binary")
load("@swf_bazel_rules_quality_rules_python//python:defs.bzl", "py_library")

py_library(
    name = "python_tool_common",
    srcs = ["python_tool_common.py"],
)

py_binary(
    name = "pylint_runner",
    srcs = ["pylint_runner.py"],
    data = ["@swf_bazel_rules_quality//quality/private/python:pylint"],
    visibility = ["//visibility:public"],
    deps = ["@swf_bazel_rules_quality//quality/private/python/tools:python_tool_common"],
)

py_binary(
    name = "black_runner",
    srcs = ["black_runner.py"],
    data = ["@swf_bazel_rules_quality//quality/private/python:black"],
    visibility = ["//visibility:public"],
    deps = ["@swf_bazel_rules_quality//quality/private/python/tools:python_tool_common"],
)

py_binary(
    name = "isort_runner",
    srcs = ["isort_runner.py"],
    data = ["@swf_bazel_rules_quality//quality/private/python:isort"],
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

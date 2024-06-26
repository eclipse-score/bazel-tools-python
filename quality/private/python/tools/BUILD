load("@swf_bazel_rules_quality_rules_python//python:defs.bzl", "py_binary", "py_library")

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

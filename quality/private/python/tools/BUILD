load("@swf_bazel_rules_quality_python//:defs.bzl", "py_binary")
load("@swf_bazel_rules_quality_rules_python//python:defs.bzl", "py_library")

py_library(
    name = "python_tool_common",
    srcs = ["python_tool_common.py"],
    visibility = ["//quality/private/python/tools:__subpackages__"],
)

py_binary(
    name = "pylint",
    srcs = ["pylint_runner.py"],
    data = ["@swf_bazel_rules_quality//quality/private/python:pylint_entry_point"],
    main = "pylint_runner.py",
    visibility = ["//visibility:public"],
    deps = ["@swf_bazel_rules_quality//quality/private/python/tools:python_tool_common"],
)

py_binary(
    name = "black",
    srcs = ["black_runner.py"],
    data = ["@swf_bazel_rules_quality//quality/private/python:black_entry_point"],
    main = "black_runner.py",
    visibility = ["//visibility:public"],
    deps = ["@swf_bazel_rules_quality//quality/private/python/tools:python_tool_common"],
)

py_binary(
    name = "isort",
    srcs = ["isort_runner.py"],
    data = ["@swf_bazel_rules_quality//quality/private/python:isort_entry_point"],
    main = "isort_runner.py",
    visibility = ["//visibility:public"],
    deps = ["@swf_bazel_rules_quality//quality/private/python/tools:python_tool_common"],
)

py_binary(
    name = "mypy",
    srcs = ["mypy_runner.py"],
    data = ["@swf_bazel_rules_quality//quality/private/python:mypy_entry_point"],
    main = "mypy_runner.py",
    visibility = ["//visibility:public"],
    deps = ["@swf_bazel_rules_quality//quality/private/python/tools:python_tool_common"],
)

py_binary(
    name = "ruff_check",
    srcs = ["ruff_check_runner.py"],
    main = "ruff_check_runner.py",
    visibility = ["//visibility:public"],
    deps = [
        "@swf_bazel_rules_quality//quality/private/python:ruff_entry_point",
        "@swf_bazel_rules_quality//quality/private/python/tools:python_tool_common",
    ],
)

py_binary(
    name = "ruff_format",
    srcs = ["ruff_format_runner.py"],
    main = "ruff_format_runner.py",
    visibility = ["//visibility:public"],
    deps = [
        "@swf_bazel_rules_quality//quality/private/python:ruff_entry_point",
        "@swf_bazel_rules_quality//quality/private/python/tools:python_tool_common",
    ],
)

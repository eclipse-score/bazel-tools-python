load("@rules_python//python:defs.bzl", "py_library")
load("@swf_bazel_rules_quality//quality:defs.bzl", "py_pytest")
load("@swf_bazel_rules_quality_pip_hub//:loaders.bzl", "pkg")

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
        "@swf_bazel_rules_quality//quality/private/python/tools:python_tool_common",
        pkg("pytest"),
    ],
)

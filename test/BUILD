load("@bazel_tools_python//quality:defs.bzl", "py_pytest", "python_tool_config")
load("@rules_python//python:defs.bzl", "py_binary", "py_library")
load("@test_pip_hub//:loaders.bzl", "pkg")

################
# Config pytest.
################

python_tool_config(
    name = "quality_python_default_config",
    config = "//:awesome_pyproject",
    visibility = ["//visibility:public"],
)

label_flag(
    name = "quality_pytest_config",
    build_setting_default = "//:quality_python_default_config",
    visibility = ["//visibility:public"],
)

py_pytest(
    name = "dummy_pytest",
    srcs = ["dummy_pytest.py"],
)

py_library(
    name = "py_custom_test_deps",
    visibility = ["//visibility:public"],
    deps = [
        pkg("pytest"),
        pkg("pytest-loop"),
    ],
)

filegroup(
    name = "awesome_pyproject",
    srcs = ["awesome_pyproject.toml"],
    visibility = ["//visibility:public"],
)

######################
# Python test targets.
######################

py_binary(
    name = "dummy_bin",
    srcs = ["dummy_bin.py"],
    deps = [":dummy_lib"],
)

py_library(
    name = "dummy_lib",
    srcs = ["dummy_lib.py"],
)

py_pytest(
    name = "dummy_test",
    srcs = ["dummy_test.py"],
    deps = [":dummy_bin"],
)

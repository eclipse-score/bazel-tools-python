# Copyright 2025 The BMW Group Authors. All rights reserved.

"""Parse pip requirements files for supported python version."""

load("@bazel_tools_python_python_3_10//:defs.bzl", python_3_10_interpreter = "interpreter")
load("@bazel_tools_python_python_3_11//:defs.bzl", python_3_11_interpreter = "interpreter")
load("@bazel_tools_python_python_3_12//:defs.bzl", python_3_12_interpreter = "interpreter")
load("@bazel_tools_python_python_3_8//:defs.bzl", python_3_8_interpreter = "interpreter")
load("@bazel_tools_python_python_3_9//:defs.bzl", python_3_9_interpreter = "interpreter")
load("@rules_python//python:pip.bzl", "pip_parse")

def python_pip_parse():
    """Parse pip requirements files for supported python version."""

    # We can't dynamically load the interpreters so the following dict versions need to match
    # "@bazel_tools_python//bazel/toolchains/python:versions.bzl%PYTHON_VERSIONS"
    # buildifier: disable=unsorted-dict-items
    python_versions = {
        "3.8": python_3_8_interpreter,
        "3.9": python_3_9_interpreter,
        "3.10": python_3_10_interpreter,
        "3.11": python_3_11_interpreter,
        "3.12": python_3_12_interpreter,
    }

    for version in python_versions:
        pip_parse(
            name = "bazel_tools_python_pip_{}".format(version.replace(".", "_")),
            requirements_lock = "@bazel_tools_python//third_party/pip:requirements_lock_{}.txt".format(version.replace(".", "_")),
            python_interpreter_target = python_versions[version],
            extra_pip_args = ["--no-cache-dir"],
        )

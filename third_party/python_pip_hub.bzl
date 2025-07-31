# Copyright 2025 The BMW Group Authors. All rights reserved.

"""Load and configure all pip requirements."""

load("@bazel_tools_python//bazel/rules:rules_python_pip_hub.bzl", "rules_python_pip_hub")
load("@bazel_tools_python//bazel/toolchains/python:versions.bzl", "PYTHON_VERSIONS")
load("@bazel_tools_python_pip_3_8//:requirements.bzl", pip_install_deps_py_3_8 = "install_deps")  # buildifier: disable=out-of-order-load
load("@bazel_tools_python_pip_3_9//:requirements.bzl", pip_install_deps_py_3_9 = "install_deps")  # buildifier: disable=out-of-order-load
load("@bazel_tools_python_pip_3_10//:requirements.bzl", pip_install_deps_py_3_10 = "install_deps")  # buildifier: disable=out-of-order-load
load("@bazel_tools_python_pip_3_11//:requirements.bzl", pip_install_deps_py_3_11 = "install_deps")  # buildifier: disable=out-of-order-load
load("@bazel_tools_python_pip_3_12//:requirements.bzl", pip_install_deps_py_3_12 = "install_deps")  # buildifier: disable=out-of-order-load

def python_pip_hub():
    """Load all rules python pip hub and configure our custom pip hub."""

    pip_install_deps_py_3_8()
    pip_install_deps_py_3_9()
    pip_install_deps_py_3_10()
    pip_install_deps_py_3_11()
    pip_install_deps_py_3_12()

    rules_python_pip_hub(
        name = "bazel_tools_python_pip_hub",
        deps_to_config_map = {
            "@bazel_tools_python_pip_{}".format(version.replace(".", "_")): "@bazel_tools_python//bazel/toolchains/python:python_{}".format(version.replace(".", "_"))
            for version in PYTHON_VERSIONS
        },
        requirements_in = "@bazel_tools_python//third_party/pip:requirements.in",
    )

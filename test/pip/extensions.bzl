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
"""Collection of the repository thid-party dependencies"""

load("@bazel_tools_python//bazel/rules:rules_python_pip_hub.bzl", _rules_python_pip_hub = "rules_python_pip_hub")
load("@bazel_tools_python//bazel/toolchains/python:versions.bzl", "PYTHON_VERSIONS")

def _rules_python_pip_hub_impl():
    """Make non module rules_python_pip_hub dependencies known to bazel."""

    _rules_python_pip_hub(
        name = "test_pip_hub",
        deps_to_config_map = {
            "@test_pip_{}".format(version.replace(".", "_")): "@bazel_tools_python//bazel/toolchains/python:python_{}".format(version.replace(".", "_"))
            for version in PYTHON_VERSIONS
        },
        requirements_in = "@bazel_tools_python_test//pip:requirements.in",
    )

rules_python_pip_hub = module_extension(lambda ctx: _rules_python_pip_hub_impl())

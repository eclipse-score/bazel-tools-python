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
load("@bazel_tools_python//quality:defs.bzl", "py_pytest")
load("@rules_python//python:defs.bzl", "py_library")
load("@single_pip_hub//:loaders.bzl", "pkg")

###################
# Configure pytest.
###################

py_library(
    name = "py_custom_test_deps",
    visibility = ["//visibility:public"],
    deps = [
        pkg("pytest"),
        pkg("pytest-loop"),
    ],
)

######################
# Python test targets.
######################

# unittest based test.
py_pytest(
    name = "dummy_test_single_version",
    srcs = ["dummy_test_single_version.py"],
    deps = ["//:dummy_bin_single_version"],
)

# pytest based test.
py_pytest(
    name = "dummy_pytest_single_version",
    srcs = ["dummy_pytest_single_version.py"],
)

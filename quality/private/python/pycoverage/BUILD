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

load("@bazel_tools_python_pip_hub//:loaders.bzl", "pkg")
load("@rules_python//python:defs.bzl", "py_binary")

package(default_visibility = ["//visibility:public"])

py_binary(
    name = "report_generator",
    srcs = ["report_generator.py"],
    visibility = ["//:__subpackages__"],
    deps = [
        pkg("termcolor"),
        pkg("coverage"),
    ],
)

py_binary(
    name = "output_generator",
    srcs = ["output_generator.py"],
    visibility = ["//:__subpackages__"],
    deps = [pkg("termcolor")],
)

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
load("@bazel_tools_python_pip_hub//:loaders.bzl", "pkg")

py_pytest(
    name = "test_pycoverage_report_generator",
    srcs = ["test_pycoverage_report_generator.py"],
    data = glob(["data/**"]),
    deps = [
        "@bazel_tools_python//quality/private/python/pycoverage:report_generator",
        pkg("coverage"),
    ],
)

py_pytest(
    name = "test_pycoverage_output_generator",
    srcs = ["test_pycoverage_output_generator.py"],
    data = glob(["data/**"]),
    deps = [
        "@bazel_tools_python//quality/private/python/pycoverage:output_generator",
        pkg("coverage"),
    ],
)

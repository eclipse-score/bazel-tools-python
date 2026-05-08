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
load("@bazel_tools_python//quality:defs.bzl", "python_tool_config")
load("@rules_python//python:defs.bzl", "py_binary", "py_library")

#################
# Config project.
#################

python_tool_config(
    name = "quality_python_default_config",
    config = "//:pyproject_toml",
    visibility = ["//visibility:public"],
)

label_flag(
    name = "quality_pytest_config",
    build_setting_default = "//:quality_python_default_config",
    visibility = ["//visibility:public"],
)

filegroup(
    name = "pyproject_toml",
    srcs = ["pyproject.toml"],
    visibility = ["//visibility:public"],
)

#################
# Python targets.
#################

py_binary(
    name = "dummy_bin_single_version",
    srcs = ["dummy_bin_single_version.py"],
    visibility = ["//tests:__subpackages__"],
    deps = [":dummy_lib_single_version"],
)

py_library(
    name = "dummy_lib_single_version",
    srcs = ["dummy_lib_single_version.py"],
)

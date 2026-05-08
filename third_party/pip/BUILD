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
load("@bazel_tools_python//bazel/toolchains/python:versions.bzl", "LEGACY_PYTHON_VERSIONS", "PYTHON_VERSIONS")
load("@bazel_tools_python//quality:defs.bzl", "pip_audit_rule")
load("@rules_python//python:pip.bzl", "compile_pip_requirements")

# Rule compile_pip_requirements handles pip requirements.
# It adds two important targets per Python version:
#  - requirements_<PYTHON_VERSION_WITH_UNDERLINE>.update: A runnable target that updates the lock file
#  - requirements_<PYTHON_VERSION_WITH_UNDERLINE>.test: A test target that validates the lock file

REQUIREMENTS_SOURCE = "requirements.in"

EXTRA_ARGS = [
    "--no-strip-extras",
    "--quiet",
]

[
    compile_pip_requirements(
        name = "requirements_{}".format(version.replace(".", "_")),
        src = REQUIREMENTS_SOURCE + ("_legacy" if version in LEGACY_PYTHON_VERSIONS else "_stable"),
        extra_args = EXTRA_ARGS,
        requirements_txt = "requirements_lock_{}.txt".format(version.replace(".", "_")),
        # Manual tag is needed because each pip requirement should be tested with its
        # matching python version. Therefore we don't want these targets to be tested
        # when targeting for example `//...` with only one python toolchain.
        tags = ["manual"],
    )
    for version in PYTHON_VERSIONS
]

[
    pip_audit_rule(
        name = "pip_audit_requirements_{}".format(version.replace(".", "_")),
        requirement = "requirements_lock_{}.txt".format(version.replace(".", "_")),
    )
    for version in PYTHON_VERSIONS
]

filegroup(
    name = "requirement_locks",
    srcs = [
        "requirements_lock_3_10.txt",
    ],
    visibility = ["//visibility:public"],
)

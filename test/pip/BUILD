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
load("@bazel_tools_python//bazel/toolchains/python:versions.bzl", "PYTHON_VERSIONS")
load("@rules_python//python:pip.bzl", "compile_pip_requirements")

# Rule compile_pip_requirements handles pip requirements.
# It has two important targets:
#  - requirements.update: A runnable target that updates the lock file
#  - requirements_test: A test target that validates the lock file

REQUIREMENTS_SOURCE = "requirements.in"

EXTRA_ARGS = [
    "--no-strip-extras",
    "--quiet",
]

[
    compile_pip_requirements(
        name = "requirements_{}".format(version.replace(".", "_")),
        src = REQUIREMENTS_SOURCE,
        extra_args = EXTRA_ARGS,
        requirements_txt = "requirements_lock_{}.txt".format(version.replace(".", "_")),
        tags = ["manual"],
    )
    for version in PYTHON_VERSIONS
]

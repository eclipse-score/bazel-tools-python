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
"""First set of internal transitive dependencies required for this module."""

load("@bazel_skylib//:workspace.bzl", "bazel_skylib_workspace")
load("@buildifier_prebuilt//:defs.bzl", "buildifier_prebuilt_register_toolchains")
load("@buildifier_prebuilt//:deps.bzl", "buildifier_prebuilt_deps")
load("@rules_python//python:repositories.bzl", "py_repositories")

def internal_transitive_dependencies():
    """Load transitive macros of the internal dependencies."""

    bazel_skylib_workspace()

    buildifier_prebuilt_deps()
    buildifier_prebuilt_register_toolchains()

    py_repositories()

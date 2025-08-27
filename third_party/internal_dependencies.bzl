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
"""Collection of the repository internal thid-party dependencies."""

load("@bazel_tools_python//third_party/bazel_skylib:bazel_skylib.bzl", "bazel_skylib")
load("@bazel_tools_python//third_party/buildifier:buildifier.bzl", "buildifier")
load("@bazel_tools_python//third_party/rules_python:rules_python.bzl", "rules_python")

def internal_dependencies():
    """Make internal third-party dependencies known to bazel."""

    bazel_skylib()
    buildifier()
    rules_python()

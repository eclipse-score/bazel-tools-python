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

"""Repository toolchain collection."""

def toolchains(name = "bazel_tools_python_toolchains"):  # buildifier: disable=unused-variable
    native.register_toolchains(
        "@bazel_tools_python//bazel/toolchains/python:all",
    )

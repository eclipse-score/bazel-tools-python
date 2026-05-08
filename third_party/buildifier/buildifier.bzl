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
"""Third-party dependency definition for buildifier."""

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

def buildifier():
    http_archive(
        name = "buildifier_prebuilt",
        sha256 = "c80b20ca1138097b5ce60bb258a6fd06ffcf7469f5f7e6722881845ff64251eb",
        strip_prefix = "buildifier-prebuilt-8.2.1.2",
        urls = ["https://github.com/keith/buildifier-prebuilt/archive/refs/tags/8.2.1.2.tar.gz"],
    )

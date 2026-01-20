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
"""Third-party dependency definition for rules_python"""

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")
load("@bazel_tools//tools/build_defs/repo:utils.bzl", "maybe")

_VERSION = "1.7.0"  # Update `README.md` if you change this.

def rules_python():
    maybe(
        http_archive,
        name = "rules_python",
        sha256 = "f609f341d6e9090b981b3f45324d05a819fd7a5a56434f849c761971ce2c47da",
        strip_prefix = "rules_python-{version}".format(version = _VERSION),
        urls = ["https://github.com/bazel-contrib/rules_python/releases/download/{version}/rules_python-{version}.tar.gz".format(version = _VERSION)],
        patches = ["@bazel_tools_python//third_party/rules_python:rules_python.patch"],
    )

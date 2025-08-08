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
"""This module defines the offered providers of the python aspect."""

PythonCollectInfo = provider(
    doc = "Collected info about the target.",
    fields = {
        "deps": ".",
        "imports": ".",
    },
)

PythonToolInfo = provider(
    doc = "Configuration structure for the python tool aspect.",
    fields = {
        "additional_features": "List of additional bazel features to be enabled when invoking python aspect.",
        "config": "Configuration file for the respective python tool.",
    },
)

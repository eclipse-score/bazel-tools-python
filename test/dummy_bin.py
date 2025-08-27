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
"""Dummy python binary that helps testing."""

import dummy_lib


def run_foo(text: str) -> str:
    """Dummy python function that helps testing."""
    dummy_lib.foo_not_allowed(text)
    return text


run_foo("foo and bar")

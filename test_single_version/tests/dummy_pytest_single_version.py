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
"""Dummy python py_pytest that helps testing."""

import pytest


def add(a, b) -> int:
    """Add function"""
    return a + b


@pytest.mark.loop(3)
def test_add_function():
    """Test add function."""

    assert add(2, 3) == 5
    assert add(2, 2) == 4
    assert add(1, 5) == 6

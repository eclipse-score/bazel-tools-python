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
"""Dummy python unittest that helps testing."""

import unittest

import dummy_bin_single_version


class TestDummyBinary(unittest.TestCase):
    """TestDummyBinary."""

    def test_run_foo(self):
        """Test run_foo function."""
        variables = ["foo", "bar"]
        for var in variables:
            assert dummy_bin_single_version.run_foo(var) == var

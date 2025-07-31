"""Dummy python unittest that helps testing."""

import unittest

import dummy_bin


class TestDummyBinary(unittest.TestCase):
    """TestDummyBinary."""

    def test_run_foo(self):
        """Test run_foo function."""
        variables = ["foo", "bar"]
        for var in variables:
            assert dummy_bin.run_foo(var) == var

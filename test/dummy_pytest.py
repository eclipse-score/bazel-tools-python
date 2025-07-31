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

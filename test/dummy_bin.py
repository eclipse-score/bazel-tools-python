"""Dummy python binary that helps testing."""

import dummy_lib


def run_foo(text: str) -> str:
    """Dummy python function that helps testing."""
    dummy_lib.foo_not_allowed(text)
    return text


run_foo("foo and bar")

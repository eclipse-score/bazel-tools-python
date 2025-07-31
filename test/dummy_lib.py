"""Dummy python library that helps testing."""


def foo_not_allowed(bar_not_allowed: str) -> str:
    """Foo function that takes bar, prints it and then returns it.

    Pylint doesn't allow foo and bar by default, therefore we appended with 'not_allowed'.
    """
    print(bar_not_allowed)
    return bar_not_allowed

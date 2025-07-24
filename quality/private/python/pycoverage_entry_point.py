"""Entry point for pycoverage.

This executes pycoverage by importing, thus executing, its main entry point.
"""

# ruff: noqa: F401
# We do not want to use __main__ but only import it.
# That is because when we import it, python already runs the tool entry point.

if __name__ == "__main__":
    from coverage import __main__  # type: ignore[import-untyped]

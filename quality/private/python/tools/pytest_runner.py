"""Pytest wrapper."""

import os
import sys

import pytest

if __name__ == "__main__":
    pytest_args = []
    pytest_args.extend(["--config-file", os.environ["_PYTEST_CONFIG_FILE"]])
    pytest_args.extend(os.environ["_PYTEST_RUNNER_TARGETS"].split(","))
    pytest_args.extend(sys.argv[1:])
    sys.exit(pytest.main(pytest_args))

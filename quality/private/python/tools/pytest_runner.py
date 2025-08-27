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

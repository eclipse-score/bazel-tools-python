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
"""Entry point for pylint python library.

This executes pylint by importing, thus executing, its main entry point.
"""

# ruff: noqa: F401
# We do not want to use __main__ but only import it.
# That is because when we import it, python already runs the tool entry point.

if __name__ == "__main__":
    from pylint import __main__  # type: ignore[import-untyped]

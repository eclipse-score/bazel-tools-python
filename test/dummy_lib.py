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
"""Dummy python library that helps testing."""


def foo_not_allowed(bar_not_allowed: str) -> str:
    """Foo function that takes bar, prints it and then returns it.

    Pylint doesn't allow foo and bar by default, therefore we appended with 'not_allowed'.
    """
    print(bar_not_allowed)
    return bar_not_allowed

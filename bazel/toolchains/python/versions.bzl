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

"""This module defines which python version are supported."""

LEGACY_PYTHON_VERSIONS = [
    "3.8",
    "3.9",
]

STABLE_PYTHON_VERSIONS = [
    "3.10",
    "3.11",
    "3.12",
    "3.13",
    "3.14",
]

PYTHON_VERSIONS = LEGACY_PYTHON_VERSIONS + STABLE_PYTHON_VERSIONS

def unsupported_python_configuration_error(custom_message):
    default_message = """
----------------------------------------------------------------------
You may be using an invalid python version configuration. 
Available options are: {py_versions}.
Please select a valid python version using rules_python's string_flag:
@rules_python//python/config_settings:python_version.
----------------------------------------------------------------------
""".format(py_versions = PYTHON_VERSIONS).rstrip()
    if custom_message:
        return """
----------------------------------------------------------------------
{custom_message}{default_message}
""".format(custom_message = custom_message, default_message = default_message)
    return default_message

def _legacy_python_warning_impl(ctx):
    """Rule that prints a warning for legacy Python versions."""
    python_version = ctx.attr.python_version

    # buildifier: disable=print
    print("⚠️ Python {} is a legacy version and may not be supported in future releases.".format(python_version))

    return [DefaultInfo()]

legacy_python_warning = rule(
    implementation = _legacy_python_warning_impl,
    attrs = {
        "python_version": attr.string(
            mandatory = True,
            doc = "The Python version string",
        ),
    },
    doc = "Rule that emits a warning for legacy Python versions during analysis.",
)

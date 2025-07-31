# Copyright 2025 The BMW Group Authors. All rights reserved.

"""This module defines which python version are supported."""

PYTHON_VERSIONS = [
    "3.8",
    "3.9",
    "3.10",
    "3.11",
    "3.12",
]

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

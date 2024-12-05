"""This module defines the offered providers of the python aspect."""

PythonCollectInfo = provider(
    doc = "Collected info about the target.",
    fields = {
        "deps": ".",
        "imports": ".",
    },
)

PythonToolInfo = provider(
    doc = "Configuration structure for the python tool aspect.",
    fields = {
        "additional_features": "List of additional bazel features to be enabled when invoking python aspect.",
        "config": "Configuration file for the respective python tool.",
    },
)

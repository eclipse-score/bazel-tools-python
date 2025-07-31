# Copyright 2025 The BMW Group Authors. All rights reserved.

"""Repository toolchain collection."""

def toolchains(name = "bazel_tools_python_toolchains"):  # buildifier: disable=unused-variable
    native.register_toolchains(
        "@bazel_tools_python//bazel/toolchains/python:all",
    )

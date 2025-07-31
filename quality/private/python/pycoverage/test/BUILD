# Copyright (C) 2025 Bayerische Motoren Werke Aktiengesellschaft (BMW AG). All rights reserved.

load("@bazel_tools_python//quality:defs.bzl", "py_pytest")
load("@bazel_tools_python_pip_hub//:loaders.bzl", "pkg")

py_pytest(
    name = "test_pycoverage_report_generator",
    srcs = ["test_pycoverage_report_generator.py"],
    data = glob(["data/**"]),
    deps = [
        "@bazel_tools_python//quality/private/python/pycoverage:report_generator",
        pkg("coverage"),
    ],
)

py_pytest(
    name = "test_pycoverage_output_generator",
    srcs = ["test_pycoverage_output_generator.py"],
    data = glob(["data/**"]),
    deps = [
        "@bazel_tools_python//quality/private/python/pycoverage:output_generator",
        pkg("coverage"),
    ],
)

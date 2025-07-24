# Copyright (C) 2025 Bayerische Motoren Werke Aktiengesellschaft (BMW AG). All rights reserved.

load("@swf_bazel_rules_quality//quality:defs.bzl", "py_pytest")
load("@swf_bazel_rules_quality_pip_hub//:loaders.bzl", "pkg")

py_pytest(
    name = "test_pycoverage_report_generator",
    srcs = ["test_pycoverage_report_generator.py"],
    data = glob(["data/**"]),
    deps = [
        "@swf_bazel_rules_quality//quality/private/python/pycoverage:report_generator",
        pkg("coverage"),
    ],
)

py_pytest(
    name = "test_pycoverage_output_generator",
    srcs = ["test_pycoverage_output_generator.py"],
    data = glob(["data/**"]),
    deps = [
        "@swf_bazel_rules_quality//quality/private/python/pycoverage:output_generator",
        pkg("coverage"),
    ],
)

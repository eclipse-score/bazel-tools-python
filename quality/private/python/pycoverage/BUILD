# Copyright (C) 2025 Bayerische Motoren Werke Aktiengesellschaft (BMW AG). All rights reserved.

load("@rules_python//python:defs.bzl", "py_binary")
load("@swf_bazel_rules_quality_pip_hub//:loaders.bzl", "pkg")

package(default_visibility = ["//visibility:public"])

py_binary(
    name = "report_generator",
    srcs = ["report_generator.py"],
    visibility = ["//:__subpackages__"],
    deps = [
        pkg("termcolor"),
        pkg("coverage"),
    ],
)

py_binary(
    name = "output_generator",
    srcs = ["output_generator.py"],
    visibility = ["//:__subpackages__"],
    deps = [pkg("termcolor")],
)

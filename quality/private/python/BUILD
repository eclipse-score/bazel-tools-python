load("@rules_python//python:defs.bzl", "py_binary")
load("@swf_bazel_rules_quality_pip_hub//:loaders.bzl", "pkg")

py_binary(
    name = "pylint_entry_point",
    srcs = ["pylint_entry_point.py"],
    visibility = ["//visibility:public"],
    deps = [pkg("pylint")],
)

py_binary(
    name = "black_entry_point",
    srcs = ["black_entry_point.py"],
    visibility = ["//visibility:public"],
    deps = [pkg("black")],
)

py_binary(
    name = "isort_entry_point",
    srcs = ["isort_entry_point.py"],
    visibility = ["//visibility:public"],
    deps = [pkg("isort")],
)

py_binary(
    name = "mypy_entry_point",
    srcs = ["mypy_entry_point.py"],
    visibility = ["//visibility:public"],
    deps = [pkg("mypy")],
)

py_binary(
    name = "ruff_entry_point",
    srcs = ["ruff_entry_point.py"],
    main = "ruff_entry_point.py",
    visibility = ["//visibility:public"],
    deps = [pkg("ruff")],
)

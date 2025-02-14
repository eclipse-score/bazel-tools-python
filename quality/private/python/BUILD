load("@rules_python//python:defs.bzl", "py_binary", "py_library")
load("@swf_bazel_rules_quality_pip_hub//:loaders.bzl", "pkg")

py_binary(
    name = "pylint_entry_point",
    srcs = ["pylint_entry_point.py"],
    visibility = ["//visibility:public"],
    deps = [pkg("pylint")],
)

py_library(
    name = "default_py_test_deps",
    visibility = ["//visibility:public"],
    deps = [
        pkg("hypothesis"),
        pkg("pytest"),
        pkg("pytest-asyncio"),
        pkg("pytest-benchmark"),
        pkg("pytest-bdd"),
        pkg("pytest-cov"),
        pkg("pytest-instafail"),
        pkg("pytest-mock"),
        pkg("pytest-rerunfailures"),
        pkg("pytest-rich"),
        pkg("pytest-timeout"),
        pkg("pytest-vcr"),
    ],
)

label_flag(
    name = "py_test_deps",
    build_setting_default = "@swf_bazel_rules_quality//quality/private/python:default_py_test_deps",
    visibility = ["//visibility:public"],
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
    deps = [
        pkg("mypy"),
        pkg("types-jsonschema"),
        pkg("types-PyYAML"),
        pkg("types-requests"),
        pkg("types-typed-ast"),
        pkg("types-six"),
        pkg("types-setuptools"),
        pkg("types-python-dateutil"),
        pkg("types-certifi"),
        pkg("types-chardet"),
        pkg("types-urllib3"),
        pkg("types-html5lib"),
    ],
)

py_binary(
    name = "ruff_entry_point",
    srcs = ["ruff_entry_point.py"],
    main = "ruff_entry_point.py",
    visibility = ["//visibility:public"],
    deps = [pkg("ruff")],
)

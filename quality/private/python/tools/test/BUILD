load("@swf_bazel_rules_quality//quality:defs.bzl", "py_pytest")

py_pytest(
    name = "test_isort_runner",
    srcs = ["test_isort_runner.py"],
    deps = ["//quality/private/python/tools:isort"],
)

py_pytest(
    name = "test_pylint_runner",
    srcs = ["test_pylint_runner.py"],
    deps = ["//quality/private/python/tools:pylint"],
)

py_pytest(
    name = "test_black_runner",
    srcs = ["test_black_runner.py"],
    deps = ["//quality/private/python/tools:black"],
)

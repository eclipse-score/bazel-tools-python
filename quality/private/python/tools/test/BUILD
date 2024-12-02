load("@swf_bazel_rules_quality_python//:defs.bzl", "py_test")

py_test(
    name = "test_isort_runner",
    srcs = ["test_isort_runner.py"],
    deps = ["//quality/private/python/tools:isort"],
)

py_test(
    name = "test_pylint_runner",
    srcs = ["test_pylint_runner.py"],
    deps = ["//quality/private/python/tools:pylint"],
)

py_test(
    name = "test_black_runner",
    srcs = ["test_black_runner.py"],
    deps = ["//quality/private/python/tools:black"],
)

load("@swf_bazel_rules_quality//third_party/pip:requirements.bzl", "requirement")
load("@swf_bazel_rules_quality_python//:defs.bzl", "py_console_script_binary")

py_console_script_binary(
    name = "pylint",
    pkg = requirement("pylint"),
    script = "pylint",
    visibility = ["//visibility:public"],
    deps = [
        requirement("astroid"),
        requirement("dill"),
        requirement("isort"),
        requirement("mccabe"),
        requirement("platformdirs"),
        requirement("tomlkit"),
    ],
)

py_console_script_binary(
    name = "black",
    pkg = requirement("black"),
    script = "black",
    visibility = ["//visibility:public"],
)

py_console_script_binary(
    name = "isort",
    pkg = requirement("isort"),
    script = "isort",
    visibility = ["//visibility:public"],
)

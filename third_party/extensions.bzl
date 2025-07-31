"""Collection of the repository thid-party extensions."""

load("@bazel_tools_python//bazel/rules:rules_python_pip_hub.bzl", _rules_python_pip_hub = "rules_python_pip_hub")
load("@bazel_tools_python//bazel/toolchains/python:versions.bzl", "PYTHON_VERSIONS")

def _rules_python_pip_hub_impl():
    """Make non module rules_python_pip_hub dependencies known to bazel."""

    _rules_python_pip_hub(
        name = "bazel_tools_python_pip_hub",
        deps_to_config_map = {
            "@bazel_tools_python_pip_{}".format(version.replace(".", "_")): "@bazel_tools_python//bazel/toolchains/python:python_{}".format(version.replace(".", "_"))
            for version in PYTHON_VERSIONS
        },
        requirements_in = "@bazel_tools_python//third_party/pip:requirements.in",
    )

rules_python_pip_hub = module_extension(lambda ctx: _rules_python_pip_hub_impl())

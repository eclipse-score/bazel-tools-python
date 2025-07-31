workspace(name = "bazel_tools_python")

##########################
# Internal dependencies. #
##########################

load("@bazel_tools_python//third_party:internal_dependencies.bzl", "internal_dependencies")

internal_dependencies()

load("@bazel_tools_python//third_party:internal_transitive_dependencies.bzl", "internal_transitive_dependencies")

internal_transitive_dependencies()

######################################
# Python toolchain and dependencies. #
######################################

load("@bazel_tools_python//third_party:python_toolchains.bzl", "python_toolchains")

python_toolchains()

load("@bazel_tools_python//bazel/toolchains:toolchains.bzl", "toolchains")

toolchains()

load("@bazel_tools_python//third_party:python_pip_parse.bzl", "python_pip_parse")

python_pip_parse()

load("@bazel_tools_python//third_party:python_pip_hub.bzl", "python_pip_hub")

python_pip_hub()

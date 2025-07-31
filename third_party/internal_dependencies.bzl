"""Collection of the repository internal thid-party dependencies."""

load("@bazel_tools_python//third_party/bazel_skylib:bazel_skylib.bzl", "bazel_skylib")
load("@bazel_tools_python//third_party/buildifier:buildifier.bzl", "buildifier")
load("@bazel_tools_python//third_party/rules_python:rules_python.bzl", "rules_python")

def internal_dependencies():
    """Make internal third-party dependencies known to bazel."""

    bazel_skylib()
    buildifier()
    rules_python()

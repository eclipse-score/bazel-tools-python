"""Third-party dependency definition for buildifier."""

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

def buildifier():
    http_archive(
        name = "buildifier_prebuilt",
        sha256 = "8ada9d88e51ebf5a1fdff37d75ed41d51f5e677cdbeafb0a22dda54747d6e07e",
        strip_prefix = "buildifier-prebuilt-6.4.0",
        urls = ["https://github.com/keith/buildifier-prebuilt/archive/refs/tags/6.4.0.tar.gz"],
    )

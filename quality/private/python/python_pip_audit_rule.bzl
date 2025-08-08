# *******************************************************************************
# Copyright (c) 2025 Contributors to the Eclipse Foundation
#
# See the NOTICE file(s) distributed with this work for additional
# information regarding copyright ownership.
#
# This program and the accompanying materials are made available under the
# terms of the Apache License Version 2.0 which is available at
# https://www.apache.org/licenses/LICENSE-2.0
#
# SPDX-License-Identifier: Apache-2.0
# *******************************************************************************
"""Executable rule that runs pip-audit on a requirements file."""

def _pip_audit_rule_impl(ctx):
    """Implementation of the pip_audit_rule.

    This rule generates a script that runs pip-audit on the specified requirements file.
    It allows for an optional index URL to be specified for the pip-audit command.
    As this rule does not resolve dependencies, files without hashes, non-locked, will only work
    with the `no-deps` option set to true.
    """

    pip_audit_tool = ctx.executable._pip_audit_tool

    script = ctx.actions.declare_file(ctx.label.name)

    requirement_file = ctx.file.requirement

    args_list = ["--disable-pip"]
    if ctx.attr.no_deps:
        args_list.append("--no-deps")
    if ctx.attr.index_url:
        args_list.extend(["--index-url", ctx.attr.index_url])
    args_list.extend(["--requirement", requirement_file.short_path])

    ctx.actions.expand_template(
        template = ctx.file._script_template,
        output = script,
        substitutions = {
            "{ARGUMENTS}": " ".join(args_list),
            "{PIP_AUDIT_TOOL}": pip_audit_tool.short_path,
        },
        is_executable = True,
    )

    runfiles = ctx.runfiles(files = [requirement_file])
    runfiles = runfiles.merge(ctx.attr._pip_audit_tool[DefaultInfo].default_runfiles)

    return [DefaultInfo(
        executable = script,
        runfiles = runfiles,
    )]

pip_audit_rule = rule(
    implementation = _pip_audit_rule_impl,
    attrs = {
        "index_url": attr.string(
            default = "",
            doc = (
                "Optional. If set, overrides the index URL used by the pip-audit command." +
                "If not provided, gets the index from the requirement file or uses the default PyPI index."
            ),
        ),
        "no_deps": attr.bool(
            default = False,
            doc = (
                "Optional. If set, pip-audit will not check for dependencies of the packages in the requirements file." +
                "Required for non-locked requirement files."
            ),
        ),
        "requirement": attr.label(
            allow_single_file = True,
            mandatory = True,
            doc = (
                "The requirement file to check for vulnerabilities, e.g., a `requirements.txt` file." +
                "Locked files, with hashes, are expected. Non locked files, without hashes, will work only with the `no-deps` option set."
            ),
        ),
        "_pip_audit_tool": attr.label(
            default = "@bazel_tools_python//quality/private/python:pip_audit_entry_point",
            executable = True,
            cfg = "exec",
            doc = "Bazel py_binary target with python's pip-audit package entry point.",
        ),
        "_script_template": attr.label(
            default = "//quality/private/python/tools:pip_audit_runner_template",
            allow_single_file = True,
            doc = "Pip-audit runner template script.",
        ),
    },
    executable = True,
)

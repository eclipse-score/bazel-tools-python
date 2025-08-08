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
"""Rule that creates an auxiliary pip hub.

Using a pip hub is already a default workflow for rules_python pip integration. We create
 our own hub to support things like multiple python toolchain and multiple platforms.

The original owner of this implementation is EF or, more precisely, Martin Medler.
Please note that this rule was still in at early, test, stage when we copied it.
If they ever use this for production it would be nice to use a common solution for both parts.

Main changes from the original version:
- `requirements.in` file lines can start with `--`;
- `_make_indirection` improved into `_generate_single_indirection` and `_generate_indirections`;
- `_generate_indirections` generate not only `pkg` but `data` target as well;
- new method `_generate_loaders` creates a `loaders.bzl` file to improve the user interface;
"""

load("@rules_python//python:pip.bzl", "pip_utils")

# Which targets from rules_python pip integration should be offered.
_INDIRECTIONS_TYPES = [
    "pkg",
    "data",
]

def _get_direct_deps(repo_ctx):
    """Read a pip requirements.in file and return a list of direct dependencies."""
    requirements = []

    lines = repo_ctx.read(repo_ctx.attr.requirements_in).split("\n")
    for line in lines:
        line = line.strip()
        if not line:
            continue  # Skip empty lines.
        if line.startswith("#"):
            continue  # Skip comments.
        if line.startswith("--"):
            continue  # Skip possible pip custom configurations.
        if "==" not in line:
            fail("Line '{}' in '{}' is missing a precise pinning via '=='.".format(line, str(repo_ctx.attr.requirements_in)) +
                 " While this is technically possible it violates our project best practices.")
        requirements.append(line.split("==", 1)[0])

    return requirements

def _generate_single_indirection(dep, deps_to_config_map, indirection_type):
    """Generate the requested dependency indirection for a given dependency to config map."""
    dep_name = pip_utils.normalize_name(dep)

    deps_map = ""
    for deps_repo, config in deps_to_config_map.items():
        deps_map += 8 * " " + '"{}": "{}//{}:{}",\n'.format(config, deps_repo, dep_name, indirection_type)

    target = """
alias(
   name = "{name}_{indirection_type}",
   actual = select({{
{map}
   }}),
   visibility = ["//visibility:public"],
)
    """.strip().format(name = dep, indirection_type = indirection_type, map = deps_map)
    return target

def _generate_indirections(repo_ctx, direct_deps):
    """Generate all indirections types for each direct dependency."""
    content = ""

    for dep in direct_deps:
        for indirection_type in _INDIRECTIONS_TYPES:
            content += _generate_single_indirection(dep, repo_ctx.attr.deps_to_config_map, indirection_type)
            content += "\n\n"

    return content

def _generate_single_loader(repo_name, indirection_type):
    """Generate the requested loader indirection."""
    return """
def {indirection_type}(package):
    return "@{name}//:{{}}_{indirection_type}".format(package)
    """.strip().format(indirection_type = indirection_type, name = repo_name)

def _generate_loaders(repo_ctx):
    """Generate all indirections types loaders."""
    content = []

    # In bazel 8 the repo names are split by + instead of ~
    # See --incompatible_use_plus_in_repo_names https://github.com/bazelbuild/bazel/issues/23127
    # However it is a hard flip since the naming is no a stable api
    use_bazel_8_repo_names = "+" in repo_ctx.name

    if use_bazel_8_repo_names:
        name_separator = "+"
    else:
        name_separator = "~"

    repo_name = repo_ctx.name.split(name_separator)[-1]

    for indirection_type in _INDIRECTIONS_TYPES:
        content.append(_generate_single_loader(repo_name, indirection_type))
    content.append("")

    return "\n\n".join(content)

def _rules_python_pip_hub_impl(repo_ctx):
    """Rules python pip hub repository implementation.

    This implementation will create a new Bazel workspace containing our custom pip hub implementation.

    Main steps are:
        - get main direct dependencies from requirements.in file;
        - create an empty WORKSPACE file;
        - create a BUILD file containing all indirection types for each dependency;
        - create a loaders.bzl file containing one loader for each indirection type;
    """
    direct_deps = _get_direct_deps(repo_ctx)

    repo_ctx.file("WORKSPACE", content = "", executable = False)
    repo_ctx.file("BUILD", content = _generate_indirections(repo_ctx, direct_deps), executable = False)
    repo_ctx.file("loaders.bzl", content = _generate_loaders(repo_ctx), executable = False)

rules_python_pip_hub = repository_rule(
    implementation = _rules_python_pip_hub_impl,
    attrs = {
        "deps_to_config_map": attr.string_dict(
            doc = """Dictionary that maps rules python pip hubs to Bazel config_settings.

This is needed so this custom pip hub can select which rules python pip hub should be selected
 according to Bazel configuration and toolchain resolution.

```
deps_to_config_map = {
            "@rules_python_pip_hub_3_10": "@your_repo_name//label/to/your:config_setting_3_10",
            "@rules_python_pip_hub_3_11": "@your_repo_name//label/to/your:config_setting_3_11",
            "@rules_python_pip_hub_3_8": "@your_repo_name//label/to/your:config_setting_3_8",
            "@rules_python_pip_hub_3_9": "@your_repo_name//label/to/your:config_setting_3_9",
        }
```

Will lead, for example, `rules_python_pip_hub_3_10` to be selected when
 `@your_repo_name//label/to/your:config_setting_3_10` conditions are met.
""",
            mandatory = True,
        ),
        "requirements_in": attr.label(
            doc = """Label of an usual pip requirements.in file.

This rule current support:
- empty lines;
- comments lines (`#`);
- configuration lines (`--`);
- and lines with versioned dependencies (<package>==<version>).
""",
            mandatory = True,
            allow_single_file = True,
        ),
    },
    doc = "Custom pip hub implementation that support multiple python toolchain and platforms.",
)

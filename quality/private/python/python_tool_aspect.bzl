"""Aspect that collects python targets dependencies and hands them to a tool runner."""

_excluded_main_label_names = [
    "rules_python_entry_point_",
]

_excluded_workspaces_roots = [
    "external/",
]

PythonToolInfo = provider(
    doc = "Configuration structure for the python tool aspect.",
    fields = {
        "config": "Configuration file for the respective python tool tool.",
    },
)

def _python_tool_config_impl(ctx):
    return [PythonToolInfo(config = ctx.file.config)]

python_tool_config = rule(
    implementation = _python_tool_config_impl,
    attrs = {
        "config": attr.label(
            allow_single_file = True,
        ),
    },
)

def _is_valid_label(label, excluded_labels, excluded_workspaces):
    """Check if a given label is valid.

    To validate a given label this functions checks its name and workspace.
    """

    for excluded_workspace_root in excluded_workspaces:
        if excluded_workspace_root in label.workspace_root:
            return False
    for excluded_label in excluded_labels:
        if excluded_label in label.name:
            return False
    return True

def _python_tool_aspect_implementation(target, ctx):
    """Python tool aspect implementation."""

    output = []

    if not PyInfo in target:
        return [OutputGroupInfo(python_tool_output = depset([]))]

    for excluded_path in _excluded_workspaces_roots:
        if excluded_path in target.label.workspace_root:
            return [OutputGroupInfo(python_tool_output = depset([]))]

    config = ctx.attr._config[PythonToolInfo].config

    sources_to_run = []
    for source in ctx.rule.attr.srcs:
        if _is_valid_label(source.label, _excluded_main_label_names, _excluded_workspaces_roots) and source.label.name.endswith(".py"):
            if source.label.package:
                sources_to_run.append(source.label.package + "/" + source.label.name)
            else:
                sources_to_run.append(source.label.name)

    if sources_to_run:
        output_file = ctx.actions.declare_file(ctx.executable._runner.basename + "_output_" + target.label.name)
        output.append(output_file)

        imports = target[PyInfo].imports.to_list()

        dependencies = ["."]
        for dep in ctx.rule.attr.deps:
            if _is_valid_label(dep.label, [], []):
                dependencies.append(dep.label.workspace_root)

        args = ctx.actions.args()
        args.use_param_file("@%s", use_always = True)
        args.set_param_file_format("multiline")

        args.add_all("--target-imports", imports, format_each = "%s")
        args.add_all("--target-dependencies", dependencies, format_each = "%s")
        args.add_all("--target-files", sources_to_run, format_each = "%s")
        args.add("--tool", ctx.executable._tool.path, format = "%s")
        args.add("--tool-config", config.path, format = "%s")
        args.add("--tool-output", output_file.path, format = "%s")
        args.add("--tool-root", ctx.expand_location(ctx.workspace_name), format = "%s")

        ctx.actions.run(
            inputs = depset([config], transitive = [target[DefaultInfo].default_runfiles.files]),
            outputs = [output_file],
            tools = [ctx.executable._runner, ctx.executable._tool, target[DefaultInfo].files_to_run],
            executable = ctx.executable._runner,
            arguments = [args],
            progress_message = "Running {tool} on: {target_name}".format(tool = ctx.executable._runner.basename, target_name = target.label.name),
        )

    return [OutputGroupInfo(python_tool_output = depset(output))]

def _python_tool_aspect(tool, runner, config):
    """Python tool aspect.

    Provides a python tool aspect instance that will call the given runner
     with the given config. The runner can then prepare its enviroment and
     call the given tool. This allows us to use this aspect with a variety
     of different python tools runners, e.g., pylint, black, ruff etc.

    Args:
        tool: tool executable, e.g., pylint, black, ruff etc.
        runner: tool runner that is invoked by this aspect and calls tool
                 with a config. Each tool requires a different runner.
        config: a provider that holds the tool config, e.g., pyproject.toml.
    Returns:
        A python tool aspect instance
    """
    return aspect(
        implementation = _python_tool_aspect_implementation,
        attrs = {
            "_config": attr.label(
                default = Label(config),
                providers = [PythonToolInfo],
            ),
            "_runner": attr.label(
                executable = True,
                cfg = "exec",
                default = Label(runner),
            ),
            "_tool": attr.label(
                executable = True,
                cfg = "exec",
                default = Label(tool),
            ),
        },
        required_providers = [PyInfo],
    )

pylint_aspect = _python_tool_aspect(
    tool = "@swf_bazel_rules_quality//quality/private/python:pylint_entry_point",
    runner = "@swf_bazel_rules_quality//quality/private/python/tools:pylint",
    config = "@swf_bazel_rules_quality//quality:quality_pylint_config",
)

black_aspect = _python_tool_aspect(
    tool = "@swf_bazel_rules_quality//quality/private/python:black_entry_point",
    runner = "@swf_bazel_rules_quality//quality/private/python/tools:black",
    config = "@swf_bazel_rules_quality//quality:quality_black_config",
)

isort_aspect = _python_tool_aspect(
    tool = "@swf_bazel_rules_quality//quality/private/python:isort_entry_point",
    runner = "@swf_bazel_rules_quality//quality/private/python/tools:isort",
    config = "@swf_bazel_rules_quality//quality:quality_isort_config",
)

mypy_aspect = _python_tool_aspect(
    tool = "@swf_bazel_rules_quality//quality/private/python:mypy",
    runner = "@swf_bazel_rules_quality//quality/private/python/tools:mypy_runner",
    config = "@swf_bazel_rules_quality//quality:quality_mypy_config",
)

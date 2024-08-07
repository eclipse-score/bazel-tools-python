"""Aspect that call a tool runner on top of a python target."""

load("@swf_bazel_rules_quality//quality/private/python:python_collect_aspect.bzl", "python_collect_aspect")
load("@swf_bazel_rules_quality//quality/private/python:python_helper.bzl", "is_valid_label")
load("@swf_bazel_rules_quality//quality/private/python:python_providers.bzl", "PythonCollectInfo", "PythonToolInfo")

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

def _python_tool_aspect_implementation(target, ctx):
    """Python tool aspect implementation."""

    output = []

    if not PyInfo in target or not is_valid_label(target.label):
        return [OutputGroupInfo(python_tool_output = depset([]))]

    config = ctx.attr._config[PythonToolInfo].config

    sources_to_run = []
    for source in ctx.rule.attr.srcs:
        if is_valid_label(source.label) and source.label.name.endswith(".py"):
            if source.label.package:
                sources_to_run.append(source.label.package + "/" + source.label.name)
            else:
                sources_to_run.append(source.label.name)

    if sources_to_run:
        output_file = ctx.actions.declare_file(ctx.executable._runner.basename + "_output_" + target.label.name + ".txt")
        output.append(output_file)

        deps = getattr(target[PythonCollectInfo], "deps")
        imports = getattr(target[PythonCollectInfo], "imports")

        args = ctx.actions.args()
        args.use_param_file("@%s", use_always = True)
        args.set_param_file_format("multiline")

        args.add_all("--target-imports", imports, format_each = "%s")
        args.add_all("--target-dependencies", deps, format_each = "%s")
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
        required_aspect_providers = [PythonCollectInfo],
        requires = [python_collect_aspect],
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
    tool = "@swf_bazel_rules_quality//quality/private/python:mypy_entry_point",
    runner = "@swf_bazel_rules_quality//quality/private/python/tools:mypy",
    config = "@swf_bazel_rules_quality//quality:quality_mypy_config",
)

ruff_check_aspect = _python_tool_aspect(
    tool = "@swf_bazel_rules_quality//quality/private/python:ruff_entry_point",
    runner = "@swf_bazel_rules_quality//quality/private/python/tools:ruff_check",
    config = "@swf_bazel_rules_quality//quality:quality_ruff_config",
)

ruff_format_aspect = _python_tool_aspect(
    tool = "@swf_bazel_rules_quality//quality/private/python:ruff_entry_point",
    runner = "@swf_bazel_rules_quality//quality/private/python/tools:ruff_format",
    config = "@swf_bazel_rules_quality//quality:quality_ruff_config",
)

"""Aspect that collects python targets information and output it to a provider."""

load("@bazel_tools_python//quality/private/python:python_helper.bzl", "is_valid_label")
load("@bazel_tools_python//quality/private/python:python_providers.bzl", "PythonCollectInfo")

def _get_collect_transitive_outputs(ctx):
    deps = []
    imports = []
    if hasattr(ctx.rule.attr, "deps"):
        for dep in ctx.rule.attr.deps:
            if hasattr(dep, "PythonCollectInfo"):
                deps.append(dep[PythonCollectInfo].deps)
                imports.append(dep[PythonCollectInfo].imports)
    return deps, imports

def _python_collect_aspect_implementation(target, ctx):
    transitive_deps, transitive_imports = _get_collect_transitive_outputs(ctx)

    if not PyInfo in target or not is_valid_label(target.label):
        return [PythonCollectInfo(
            deps = depset([], transitive = transitive_deps),
            imports = depset([], transitive = transitive_imports),
        )]

    imports = target[PyInfo].imports.to_list()

    deps = ["."]
    if ctx.rule.attr.deps:
        deps.append("external")
    for dep in ctx.rule.attr.deps:
        deps.append(dep.label.workspace_root)

    return [PythonCollectInfo(
        deps = depset(deps, transitive = transitive_deps),
        imports = depset(imports, transitive = transitive_imports),
    )]

def _python_collect_aspect():
    return aspect(
        implementation = _python_collect_aspect_implementation,
        attr_aspects = ["deps"],
        attrs = {},
        provides = [PythonCollectInfo],
    )

python_collect_aspect = _python_collect_aspect()

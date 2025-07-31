# Python

This module offers a set of Bazel integrated, fully cacheable and configurable Python quality tools and test frameworks.

- [Python](#python)
  - [Python Tools](#python-tools)
    - [How to use](#how-to-use)
    - [Basic Usage](#basic-usage)
    - [Available Tools](#available-tools)
      - [Black](#black)
      - [Isort](#isort)
      - [Mypy](#mypy)
      - [Pylint](#pylint)
      - [Ruff-check](#ruff-check)
      - [Ruff-format](#ruff-format)
    - [Extra Features](#extra-features)
  - [Custom Pytest](#custom-pytest)
    - [Configuration](#configuration)
    - [How to use](#how-to-use-1)

## Python Tools

Bazel Rules Quality has multiple Bazel integrated [available tools](#available-tools) to check and refactor our Bazel users Python code.

### How to use

Each tool uses the same [default python configuration](quality/BUILD#L58). One can configure each tool separately or, preferably, chose to create a single custom configuration for every tool.
To achieve that, a custom configuration rule must be created using the [`python_tool_config`](quality/defs.bzl#L24) rule. The file referenced by `python_tool_config` can be, for example, a `pyproject.toml` file containing one section for each selected tool. Our [default configuration file](/quality/private/python/support/pyproject.toml) can be used as template.

```py
# path/to/BUILD
load("@bazel_tools_python//quality:defs.bzl", "python_tool_config")
filegroup(
    name = "pyproject_toml",
    srcs = ["pyproject.toml"],
    visibility = ["//visibility:public"],
)
python_tool_config(
    name = "custom_config",
    config = ":pyproject_toml",
    visibility = ["//visibility:public"],
)
Finally, each selected tool configuration can be overloaded with the newly created custom configuration target.  target overload shortcut can be added to the `.bazelrc` file:

# .bazelrc
build:pylint --@bazel_tools_python//quality:quality_pylint_config=//path/to:pylint_config
build:mypy --@bazel_tools_python//quality:quality_mypy_config=//path/to:python_config
build:black --@bazel_tools_python//quality:quality_black_config=//path/to:python_config
build:isort --@bazel_tools_python//quality:quality_isort_config=//path/to:python_config
build:ruff_check --@bazel_tools_python//quality:quality_ruff_config=//path/to:python_config
build:ruff_format --@bazel_tools_python//quality:quality_ruff_config=//path/to:python_config
```

### Basic Usage

To run one or more tools, considering that they are correctly configured, you can use the following commands:

```bash
bazel build --config=black --keep_going [--features=refactor] -- //...
bazel build --config=isort --keep_going [--features=refactor] -- //...
bazel build --config=mypy --keep_going -- //...
bazel build --config=pylint --keep_going -- //...
bazel build --config=ruff_check --keep_going [--features=refactor] -- //...
bazel build --config=ruff_format --keep_going [--features=refactor] -- //...
```

Where `--features=refactor` is optional if you want the targets to be refactored automatically by the tool.
See section [Refactoring](#refactoring) below for more details.

Finally in the `.bazelrc` file we can configure the build for each tool.

```py
# .bazelrc

build:pylint --output_groups=python_tool_output
build:pylint --aspects=@bazel_tools_python//quality:defs.bzl%pylint_aspect

build:black --output_groups=python_tool_output
build:black --aspects=@bazel_tools_python//quality:defs.bzl%black_aspect

build:isort --output_groups=python_tool_output
build:isort --aspects=@bazel_tools_python//quality:defs.bzl%isort_aspect

build:mypy --output_groups=python_tool_output
build:mypy --aspects=@bazel_tools_python//quality:defs.bzl%mypy_aspect

build:ruff_check --output_groups=python_tool_output
build:ruff_check --aspects=@bazel_tools_python//quality:defs.bzl%ruff_check_aspect
build:ruff_format --output_groups=python_tool_output
build:ruff_format --aspects=@bazel_tools_python//quality:defs.bzl%ruff_format_aspect
```

### Available Tools

#### Black

Black is the uncompromising Python code formatter. By using it, you agree to cede control over minutiae of hand-formatting.

For more information read [black documentation](https://black.readthedocs.io/en/stable/).

#### Isort

Isort is a Python utility / library to sort imports alphabetically and automatically separate into sections and by type.

For more information read [Isort documentation](https://pycqa.github.io/isort/).

#### Mypy

Mypy is a static type checker for Python. Type checkers help ensure that you're using variables and functions in your code correctly. With mypy, add type hints ([PEP 484](https://www.python.org/dev/peps/pep-0484/)) to your Python programs, and mypy will warn you when you use those types incorrectly.

For more information read [Mypy documentation](https://mypy.readthedocs.io/en/stable/).

#### Pylint

Pylint is a static code analyser for Python 2 or 3. Pylint analysis your code without actually running it. It checks for errors, enforces a coding standard, look for code smells, and can make suggestions about how the code could be refactored.

For more information read [Pylint documentation](https://pylint.readthedocs.io/en/stable/).

#### Ruff-check

Ruff is an extremely fast Python linter designed as a drop-in replacement for Flake8 (plus dozens of plugins), isort, pydocstyle, pyupgrade, autoflake, and more. Ruff check is the primary entrypoint to the Ruff linter.

For more information read [Ruff check documentation](https://docs.astral.sh/ruff/linter/).

#### Ruff-format

The Ruff formatter is an extremely fast Python code formatter designed as a drop-in replacement for Black, available as part of the ruff CLI via ruff format. Ruff format is the primary entrypoint to the formatter.

For more information read [Ruff formatter documentation](https://docs.astral.sh/ruff/formatter/).

### Refactoring

Some tools have an extra feature called `refactor`. When used with the CLI command, the tool will fix most findings that have been found in the target file. The tools that have this feature are: `black`, `isort`, `ruff-check` and `ruff-format`. Note that `ruff-check` may not automatically fix all findings.

To use the `refactor` feature, one must add `--features=refactor` to the command line. For example:

```py
bazel build --config=black --keep_going --features=refactor -- //...
bazel build --config=isort --keep_going --features=refactor -- //...
bazel build --config=ruff_check --keep_going --features=refactor -- //...
bazel build --config=ruff_format --keep_going --features=refactor -- //...
```

## Pip-audit rule

A custom Bazel rule which generates a script that runs `pip-audit` on the specified requirements file.

This helps validate vulnerabilities that a certain set of Python requirements might have, which is a good practice and also required for qualification purposes.

For more information, read the [pip-audit documentation](https://pypi.org/project/pip-audit/).

### Configuration

The rule supports the following attributes:

- `requirement`: Mandatory. The requirement file to check for vulnerabilities, e.g., a `requirements.txt` file. Locked files with hashes are expected. Non-locked files without hashes will work only with the `no_deps` option set.
- `no_deps`: Optional. Defaults to `False`. If set, pip-audit will not check for dependencies of the packages in the requirements file. Required for non-locked requirement files.
- `index_url`: Optional. If set, overrides the index URL used by the pip-audit command. If not provided, gets the index from the requirement file or uses the default PyPI index.

### How to use

To use the pip-audit rule, load it from the quality module and create a target with your requirements file:

```starlark
# BUILD
load("@bazel_tools_python//quality:defs.bzl", "pip_audit_rule")

pip_audit_rule(
  name = "pip_audit",
  requirement = "requirements.txt",
)
```

To run the respective target:

```bash
bazel run //:pip_audit
```

In case of multiple requirements files, it is necessary to create multiple rules and execute each one of them.

## Custom Pytest

Bazel's default [pytest rule](https://bazel.build/reference/be/python#py_test) rule was not designed specifically for [Python's pytest](https://github.com/pytest-dev/pytest). Therefore, one has to do some additional scripting in order to use pytest framework with Python adn Bazel.

To improve Python coding experience with Bazel, a custom `py_pytest` rule is offered by Bazel Rules Quality.

### Configuration

Following the same configuration flow as the [Python tools](#python-tools), it is possible to configure the custom `py_pytest` rule by overriding [quality_pytest_config](/quality/BUILD#L65) label. In a similar fashion, the `py_pytest` default dependencies can also be modified by overriding [py_test_deps](/quality/private/python/BUILD#L30) label.

To use a custom configuration file, one can add the following command line in the `.bazelrc`:

```bash
# .bazelrc
build --@bazel_tools_python//quality:quality_pytest_config=//quality/private/python/support:awesome_pyproject
```

To use a custom default dependency list, one can add the following command line in the `.bazelrc`:

```bash
# .bazelrc
build --@bazel_tools_python//quality/private/python:py_test_deps=//:py_custom_test_deps
```

### How to use

The custom `py_pytest` rule is basically a drop-in replacement to Bazel's default `pytest` rule. To utilize it, one has to load `py_pytest` and then create a test target with it. For example:

```bash
# BUILD
load("@bazel_tools_python//quality:defs.bzl", "py_pytest")

py_pytest(
    name = "test_dummy",
    srcs = ["dummy.py"],
    deps = ["dummy_lib"],
)
```

It's only necessary to import the `pytest` when used in the test file.

Finally run the bazel command to run the test.

```bash
bazel test //:test_dummy
```

If any of the tests are failing, an error message will be reported in the terminal and/or in an report file.

There is also a possibility to use test arguments with the bazel command, for example:

```bash
bazel test //... --test_arg=[argument]
```

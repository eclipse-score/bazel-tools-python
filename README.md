# Bazel Rules Quality Python (bazel_tools_python)

This repository contains bazel integrations for python quality tools.

- [Offered Tools](#offered-tools)
- [How to use bazel_tools_python](#how-to-use-bazel-tools-python)
  - [Requirements](#requirements)
  - [Select python pip hub version](#select-python-pip-hub-version)
  - [Using WORKSPACE](#using-workspace)
  - [Using bzlmod](#using-bzlmod)
- [Contributing](#contributing)

## Offered Tools

Each offered tool has it own README document and can be independently activated and configured.

| Tool                                            | Tool Type               | Bazel Type | Supported Languages | Workspace | Bzlmod |
| :---------------------------------------------: | :---------------------: | :--------: | :-----------------: | :-------: | :----: |
| [pylint](quality/private/python/README.md)      | Code linter             | aspect     | Python              | yes       | no     |
| [ruff-check](quality/private/python/README.md)  | Code linter             | aspect     | Python              | yes       | yes    |
| [mypy](quality/private/python/README.md)        | Code type linter        | aspect     | Python              | yes       | yes    |
| [black](quality/private/python/README.md)       | Code formatter          | aspect     | Python              | yes       | yes    |
| [ruff-format](quality/private/python/README.md) | Code formatter          | aspect     | Python              | yes       | yes    |
| [isort](quality/private/python/README.md)       | Import formatter        | aspect     | Python              | yes       | yes    |
| [pytest](quality/private/python/README.md)      | Test Framework          | aspect     | Python              | yes       | yes    |
| [pycoverage](quality/private/python/README.md)  | Code coverage tool      | aspect     | Python              | yes       | yes    |
| [pip_audit](quality/private/python/README.md)   | Vulnerability checker   | rule       | Python              | yes       | yes    |

## How to use bazel_tools_python

The next sections explain the steps to achieve a proper config for each Bazel dependency manager. For a fully working setup, take a look at the [test workspace](test) as an example.

### Requirements

It's important to note that this repository does not supply python toolchains but only its pip dependencies. Therefore one must set up its own python toolchain. This repository support major python versions from `3.8` to `3.12`.

Additionaly, one must have the following bazel repositories already in place:

- bazel_skylib >= 1.7.1
- rules_python >= 0.40.0

### Select python pip hub version

To select the correct python dependency version one only needs to set a `string_flag` under one's `.bazelrc` file.

For example if one is using python `3.10`, one should select our python `3.10` dependencies by adding the following lines to the respective `.bazelrc` file.

```python
# .bazelrc

common --flag_alias=python=@rules_python//python/config_settings:python_version
common --python=3.10
```

### Using WORKSPACE

Add this to your `WORKSPACE` file.

```python
# WORKSPACE

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

http_archive(
    name = "bazel_tools_python",
    sha256 = "<omitted>",
    urls = ["<domain>/bazel-tools-python/<version>/bazel-tools-python-<version>.tar.gz"],
)

load("@bazel_tools_python//third_party:python_toolchains.bzl", bazel_tools_python_python_toolchains = "python_toolchains")

bazel_tools_python_python_toolchains()

load("@bazel_tools_python//third_party:python_pip_parse.bzl", bazel_tools_python_python_pip_parse = "python_pip_parse")

bazel_tools_python_python_pip_parse()

load("@bazel_tools_python//third_party:python_pip_hub.bzl", bazel_tools_python_python_pip_hub = "python_pip_hub")

bazel_tools_python_python_pip_hub()
```

### Using bzlmod

Add this to your `MODULE.bazel` file.

```python
# MODULE.bazel

bazel_dep(name = "bazel_tools_python", version = "<version>")
```

To generate Bazel integrity value, one can use the following command:

```sh
openssl dgst -sha256 -binary bazel-tools-python-<version>.tar.gz | openssl base64 -A | sed 's/^/sha256-/'
```

## Contributing

Please check our [contributing guide](CONTRIBUTING.md).

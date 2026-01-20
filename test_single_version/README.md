# Single Python Version Test Environment

This is a test environment demonstrating the Bazel Python tools configuration with a single Python version setup. It serves as a practical example of how to use the bazel-tools-python infrastructure.

> **Note:** This workspace only uses bzlmod.

## Structure

### Root Level

- **BUILD**: Defines Python binary and library targets with quality configuration setup
- **MODULE.bazel**: Module configuration specifying Python 3.14 as the single toolchain version
- **pyproject.toml**: Python project configuration with quality tool settings
- **run_all_tests.sh**: Script to execute all tests in this environment

### Python Targets

- **dummy_bin_single_version**: A simple Python binary demonstrating single-version deployment
- **dummy_lib_single_version**: A reusable Python library showing dependency management

### Dependencies

- **pip/**: Contains pip requirements management
  - `requirements.in`: Source requirements file listing package dependencies
  - `requirements_lock.txt`: Locked dependency versions for reproducible builds
  - `BUILD`: Pip compilation rules and targets
  - `extensions.bzl`: Custom Bazel extensions for dependency management

### Tests

- **tests/**: Test suite directory containing unittest and pytest tests
  - `dummy_test_single_version`: Test using unittest
  - `dummy_pytest_single_version`: Unit test demonstrating pytest integration

## Running Tests

Execute all tests and quality tools in this environment:

```bash
./run_all_tests.sh
```

## Update pip dependencies

Empty the [requirements_lock.txt](pip/requirements_lock.txt) file and run the following command to regenerate it:

```bash
bazel run //pip:requirements.update
```

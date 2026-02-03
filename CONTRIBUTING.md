# Eclipse Safe Open Vehicle Core (SCORE)

The [Eclipse Safe Open Vehicle Core](https://projects.eclipse.org/projects/automotive.score) project aims to develop an open-source core stack for Software Defined Vehicles (SDVs), specifically targeting embedded high-performance Electronic Control Units (ECUs).
Please check the [documentation](https://eclipse-score.github.io) for more information.
The source code is hosted at [GitHub](https://github.com/eclipse-score).

The communication mainly takes place via the [`score-dev` mailing list](https://accounts.eclipse.org/mailing-list/score-dev) and GitHub issues & pull requests (PR). And we have a chatroom for community discussions here [Eclipse SCORE chatroom](https://chat.eclipse.org/#/room/#automotive.score:matrix.eclipse.org).

Please note that for the project the [Eclipse Foundation’s Terms of Use](https://www.eclipse.org/legal/terms-of-use/) apply.
In addition, you need to sign the [ECA](https://www.eclipse.org/legal/ECA.php) and the [DCO](https://www.eclipse.org/legal/dco/) to contribute to the project.

## Contributing

Want to contribute? You're welcoe and we're happy to accept your pull requests!

- [Development](#development)
  - [Updating python dependencies](#updating-python-dependencies)
  - [Local quality check](#local-quality-check)

### Getting involved

#### Setup Phase

This phase is part of the eclipse Incubation Phase and shall establish all the processes needed for a safe development of functions. Only after this phase it will be possible to contribute code to the project. As the development in this project is driven by requirements, the processes and needed infrastructure incl. tooling will be established based on non-functional Stakeholder_Requirements<!-- TODO: fill link to correct page with requirements -->. During setup phase the contributions are Bug Fixes and Improvements (both on processes and infrastructure).

#### Bug Fixes and Improvements

Improvements are adding/changing processes and infrastructure, bug fixes can be also on development work products like code.
In case you want to fix a bug or contribute an improvement, please perform the following steps:

1) Create a PR by using the corresponding template ([Bugfix PR template](.github/PULL_REQUEST_TEMPLATE/bug_fix.md) or [Improvement PR template](.github/PULL_REQUEST_TEMPLATE/improvement.md)). Please mark your PR as draft until it's ready for review by the Committers (see the [Eclipse Foundation Project Handbook](https://www.eclipse.org/projects/handbook/#contributing-committers) for more information on the role definitions).
2) Initiate content review by opening a corresponding issue for the PR when it is ready for review. Review of the PR and final merge into the project repository is in responsibility of the Committers. Use the [Bugfix Issue template](.github/ISSUE_TEMPLATE/bug_fix.md) or [Improvement Issue template](.github/ISSUE_TEMPLATE/improvement.md) for this.

Please check here for our Git Commit Rules in the [Configuration_Tool_Guidelines](https://eclipse-score.github.io/score/process_description/guidelines/index.html).

Please use the [Stakeholder and Tool Requirements Template](https://eclipse-score.github.io/score/process_description/templates/index.html) when defining these requirements.

#### Additional Information

Please note, that all Git commit messages must adhere the rules described in the [Eclipse Foundation Project Handbook](https://www.eclipse.org/projects/handbook/#resources-commit).

Please find process descriptions here: [process description](https://eclipse-score.github.io/score/process_description/).

### Development

#### Updating python dependencies

This repository uses Bazel `rules_python` pip integration plus a [custom pip hub implementation](bazel/rules/rules_python_pip_hub.bzl). Therefore, to add, remove or modify python pip dependencies, one should do as follows:

1. Update the dependency and its version under [requirements.in_stable](third_party/pip/requirements.in_stable) and/or [requirements.in_legacy](third_party/pip/requirements.in_legacy) depending on which Python version the dependency is targeted to. See
    [Tool Versions](README.md#tool-versions) for more information about legacy and stable python versions;
2. Lock pip requirements by executing `bazel run //third_party/pip:update.sh`. This will update all `requirements_lock_3_*.txt` files under `third_party/pip`;
3. Test the updated requirements by executing `bazel run //third_party/pip:test.sh`.

After this was successfully done, it is possible to load pip packges into bazel targets. To load the pip dependency package itself (common use case), one can use our pip hub `pkg` alias.

```python
load("@bazel_tools_python_pip_hub//:loaders.bzl", "pkg")

py_binary(
    ...
    deps = [
        pkg("pip_package_name"),
    ],
    ...
)
```

Other options are also available through other pip hub aliases, for example, the dependency data can be accessed using the `data` alias.

#### Local quality check

Ideally, one should verify code quality locally before pushing changes to the CI. This avoids unecessary CI jobs and can even speed up development.
To do that, simply run [`scripts/run_all_tests.sh`](scripts/run_all_tests.sh) from the repo root.

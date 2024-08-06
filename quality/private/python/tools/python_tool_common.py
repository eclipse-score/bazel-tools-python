"""Common features for runners that interface the python tool aspect."""

import argparse
import dataclasses
import itertools
import os
import pathlib
import subprocess
import typing as t


class PythonPathNotFoundError(Exception):
    """Raised when it is not possible to find a target path."""

    def __init__(self, path: str, tool: str):
        self.path = path
        self.tool = tool
        super().__init__(f'The path "{self.path}" was not found. Therefore {self.tool} cannot properly run.')


class LinterFindingAsError(Exception):
    """Raised when a linter finds a finding treats it as an error."""

    def __init__(self, path: t.Union[str, pathlib.Path], tool: str):
        self.path = path
        self.tool = tool
        super().__init__(f'At least one {self.tool} finding was treated as error. See its output at "{self.path}"')


class LinterSubprocessError(Exception):
    """Raised when a linter subprocess fails."""

    def __init__(
        self,
        commands: str,
        return_code: t.Union[str, int],
        stdout: str,
        stderr: str,
    ):
        self.commands = commands
        self.return_code = return_code
        self.stdout = stdout
        self.stderr = stderr
        super().__init__(
            f'The command "{self.commands}" returned code "{self.return_code}"'
            f" and the following error message:\n{stderr or stdout}"
        )


@dataclasses.dataclass
class SubprocessInfo:
    """Class that provides a clean interface to the subprocess output."""

    stdout: str
    stderr: str
    return_code: t.Union[str, int]


def execute_subprocess(
    commands: list[str],
    cwd: pathlib.Path = pathlib.Path.cwd(),
    env: t.Optional[t.Mapping[str, str]] = None,
) -> SubprocessInfo:
    """Function that calls a subprocess and expects a zero return code."""
    try:
        result = subprocess.run(
            commands,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            text=True,
            shell=False,
            env=env or os.environ,
            cwd=cwd,
            universal_newlines=True,
        )
    except subprocess.CalledProcessError as exception:
        raise LinterSubprocessError(
            commands=str(commands),
            return_code=exception.returncode,
            stdout=exception.stdout,
            stderr=exception.stderr,
        ) from None

    return SubprocessInfo(
        stdout=result.stdout,
        stderr=result.stderr,
        return_code=result.returncode,
    )


@dataclasses.dataclass
class AspectArguments:
    """Class that provides a clean and verified interface between aspect and runner."""

    target_imports: set[pathlib.Path]
    target_dependencies: set[pathlib.Path]
    target_files: set[pathlib.Path]
    tool: pathlib.Path
    tool_config: pathlib.Path
    tool_output: pathlib.Path
    tool_root: str

    def __post_init__(self):
        def resolve_paths(paths: list[str], prepend_path: str = "") -> set[pathlib.Path]:
            resolved_paths = set()
            for path in paths:
                try:
                    if pathlib.Path(path).is_relative_to(self.tool_root):
                        # This is the usual branch for local files or libraries.
                        # The code go through here when path is relative to the sandbox root.
                        resolved_paths.add(pathlib.Path(path).relative_to(self.tool_root).resolve(strict=True))
                    else:
                        # This is the usual branch for third-party files or libraries.
                        # The code go through here when path is not directly relative to sandbox root.
                        # Instead, a given prepend_path is prepended to path.
                        resolved_paths.add((pathlib.Path(prepend_path) / path).resolve(strict=True))
                except FileNotFoundError as exception:
                    # Before throwing an exception, a check for bazel generated files is made.
                    # For that, a glob for every Bazel compilation mode pattern prepended to path is done.
                    modes = ["fastbuild", "dbg", "opt"]
                    try:
                        resolved_path = next(
                            itertools.chain.from_iterable(
                                pathlib.Path.cwd().glob(f"bazel-out/k8-{mode}/bin/{path}") for mode in modes
                            )
                        )
                    except StopIteration as _:
                        # If it doesn't exists, throw an exception.
                        raise PythonPathNotFoundError(
                            path=exception.filename,
                            tool=self.tool.name,
                        ) from None
                    # If it exists, add it to the resolved_paths list and continue.
                    resolved_paths.add(resolved_path)
            return resolved_paths

        self.target_imports = resolve_paths(self.target_imports, "external")
        self.target_dependencies = resolve_paths(self.target_dependencies)
        self.target_files = resolve_paths(self.target_files)


def parse_args() -> AspectArguments:
    """Parse and return arguments."""
    parser = argparse.ArgumentParser(fromfile_prefix_chars="@")

    parser.add_argument(
        "--target-imports",
        type=str,
        action="extend",
        nargs="+",
        default=[],
        help="",
    )
    parser.add_argument(
        "--target-dependencies",
        type=str,
        action="extend",
        nargs="+",
        default=[],
        help="",
    )
    parser.add_argument(
        "--target-files",
        type=str,
        action="extend",
        nargs="+",
        default=[],
        help="",
    )
    parser.add_argument(
        "--tool",
        type=pathlib.Path,
        required=True,
        help="",
    )
    parser.add_argument(
        "--tool-config",
        type=pathlib.Path,
        required=True,
        help="",
    )
    parser.add_argument(
        "--tool-output",
        type=pathlib.Path,
        required=True,
        help="",
    )
    parser.add_argument(
        "--tool-root",
        type=str,
        required=True,
        help="",
    )

    return AspectArguments(**vars(parser.parse_args()))

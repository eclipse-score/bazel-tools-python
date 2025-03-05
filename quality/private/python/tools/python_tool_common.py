"""Common features for runners that interface the python tool aspect."""

import argparse
import dataclasses
import enum
import itertools
import json
import os
import pathlib
import subprocess
import typing as t


@enum.unique
class Severity(str, enum.Enum):
    """Enum for severity types."""

    WARN = "WARN"
    ERROR = "ERROR"
    INFO = "INFO"


class FindingsJSONEncoder(json.JSONEncoder):
    """Encodes dataclass objects using asdict and other objects as strings."""

    def default(self, o):
        """Overrides default encoding."""
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return str(o)


@dataclasses.dataclass
class Finding:
    """Defines a finding."""

    path: pathlib.Path
    message: str
    severity: Severity
    tool: str
    rule_id: str
    line: int = 1
    column: int = 1

    def __str__(self):
        output = f"{self.path}"
        output += f":{self.line}" if self.line else ""
        output += f":{self.column}" if self.line and self.column else ""
        output += f": {self.message} [{self.tool}:{self.rule_id}]"
        return output


class Findings(t.List[Finding]):
    """Defines a list of findings."""

    def to_text_file(self, file: pathlib.Path) -> None:
        """Dumps a list of findings to a .txt file."""
        file.write_text(str(self), encoding="utf-8")

    def to_json_file(self, file: pathlib.Path) -> None:
        """Dumps a list of findings to a .json file."""
        file.write_text(json.dumps(self, cls=FindingsJSONEncoder, indent=2), encoding="utf-8")

    def __str__(self) -> str:
        return "\n".join([str(finding) for finding in self])


class PythonPathNotFoundError(Exception):
    """Raised when it is not possible to find a target path."""

    def __init__(self, path: str, tool: str):
        self.path = path
        self.tool = tool
        super().__init__(f'The path "{self.path}" was not found. Therefore {self.tool} cannot properly run.')


class LinterFindingAsError(SystemExit):
    """Raised when a linter finds a finding treats it as an error."""

    def __init__(self, tool_name: str, findings: Findings, outputs: t.List[pathlib.Path]):
        self.findings = findings
        message = f'\nTool "{tool_name}" found findings and stored them at:\n- '
        message += "\n- ".join([str(output) for output in outputs])
        message += f"\nThe following findings were found:\n{self.findings}\n"
        super().__init__(message)


class LinterSubprocessError(Exception):
    """Raised when a linter subprocess fails."""

    def __init__(
        self,
        commands: t.List[str],
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
    commands: t.List[str],
    cwd: pathlib.Path = pathlib.Path.cwd(),
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
            cwd=cwd,
            universal_newlines=True,
        )
    except subprocess.CalledProcessError as exception:
        raise LinterSubprocessError(
            commands=commands,
            return_code=exception.returncode,
            stdout=exception.stdout,
            stderr=exception.stderr,
        ) from None

    return SubprocessInfo(
        stdout=result.stdout,
        stderr=result.stderr,
        return_code=result.returncode,
    )


def _is_relative_to(path: pathlib.Path, root: pathlib.Path):
    """Helper function that mimics what pathlib.Path.is_relative_to does.

    This is needed to ensure support for python 3.8.
    """
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


@dataclasses.dataclass
class AspectArguments:  # pylint: disable=too-many-instance-attributes
    """Class that provides a clean and verified interface between aspect and runner."""

    target_imports: t.Set[pathlib.Path]
    target_dependencies: t.Set[pathlib.Path]
    target_files: t.Set[pathlib.Path]
    tool: pathlib.Path
    tool_config: pathlib.Path
    tool_output_text: pathlib.Path
    tool_output_json: pathlib.Path
    tool_root: str
    refactor: bool

    def __post_init__(self):
        def resolve_paths(paths: t.List[str], prepend_path: str = "") -> t.Set[pathlib.Path]:
            resolved_paths = set()
            for path in paths:
                try:
                    if _is_relative_to(pathlib.Path(path), pathlib.Path(self.tool_root)):
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

        env = os.environ
        for target_import in self.target_imports | self.target_dependencies:
            if "PYTHONPATH" not in env:
                env["PYTHONPATH"] = str(target_import)
            else:
                env["PYTHONPATH"] += os.pathsep + str(target_import)


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
        "--tool-output-text",
        type=pathlib.Path,
        required=True,
        help="",
    )
    parser.add_argument(
        "--tool-output-json",
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
    parser.add_argument(
        "--refactor",
        type=bool,
        default=False,
        help="",
    )

    return AspectArguments(**vars(parser.parse_args()))


def execute_runner(
    get_command: t.Callable[[AspectArguments], t.List[str]],
    output_parser: t.Callable[[SubprocessInfo], Findings],
    exception_handler: t.Optional[t.Callable[[LinterSubprocessError], SubprocessInfo]] = None,
) -> None:
    """Handles running the tool subprocess, checking its return and outputing the findings.

    :param get_command:
        Function that returns the command to run the tool.
    :param output_parser:
        Function that receives SubprocessInfo, process it and returns Findings.
    :param exception_handler:
        Function that handles the cases that the tool has a non-zero return code.
    """
    args = parse_args()

    tool_name = args.tool.name.split("_entry_point")[0]
    subprocess_list = get_command(args)

    try:
        tool_output = execute_subprocess(subprocess_list)

    except LinterSubprocessError as exception:
        if exception_handler:
            tool_output = exception_handler(exception)
        else:
            raise exception

    findings = output_parser(tool_output)

    findings.to_text_file(args.tool_output_text)
    findings.to_json_file(args.tool_output_json)
    if findings:
        raise LinterFindingAsError(
            tool_name=tool_name,
            findings=findings,
            outputs=[
                args.tool_output_text,
                args.tool_output_json,
            ],
        )

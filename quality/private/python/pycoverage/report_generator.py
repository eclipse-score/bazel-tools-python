# Copyright (C) 2025 Bayerische Motoren Werke Aktiengesellschaft (BMW AG). All rights reserved.

"""Custom coverage report generator for pycoverage."""

import argparse
import logging
import sys
from pathlib import Path
from pprint import pformat

from coverage import Coverage
from termcolor import colored


def coverage_file(line: str) -> bool:
    """Check if the given string is a path to a coverage.dat file."""

    file = Path(line)

    return file.parts[-1] == "coverage.dat" and file.stat().st_size != 0


def main() -> int:
    """Main entry point."""
    logging.basicConfig(level=logging.INFO)
    logging.info(colored("Running report-generator on all executed tests", "magenta"))

    args = parse_args()
    logging.debug(msg=f"Arguments:\n{pformat(args)}")

    # Always create an output file to avoid bazel errors.
    args.output_file.touch()

    # Read the reports file
    coverage_files = []
    with open(args.reports_file, encoding="utf-8") as reports_file:
        coverage_files = list(filter(coverage_file, map(lambda line: line.strip(), reports_file.readlines())))

    if not coverage_files:
        logging.error("No python coverage reports found.")
        return 0

    # Combine the coverage data
    logging.debug(f"Combining coverage data from {len(coverage_files)} files.")
    cov = Coverage(data_file=args.output_file)
    cov.combine(data_paths=coverage_files, keep=True)
    cov.save()

    return 0


def parse_args() -> argparse.Namespace:
    """Parse args."""

    parser = argparse.ArgumentParser()

    parser.add_argument("--output_file", type=Path)
    parser.add_argument("--reports_file", type=Path)

    return parser.parse_args()


if __name__ == "__main__":
    sys.exit(main())

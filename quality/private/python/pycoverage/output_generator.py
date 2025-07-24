# Copyright (C) 2025 Bayerische Motoren Werke Aktiengesellschaft (BMW AG). All rights reserved.

"""Custom coverage report generator for pycoverage."""

import argparse
import logging
import os
import shutil
import sys
from pathlib import Path
from pprint import pformat

from termcolor import colored


def main() -> None:
    """Main entry point."""
    logging.basicConfig(level=logging.INFO)
    logging.info(colored("Running MERGER on all executed tests", "magenta"))

    args = parse_args()
    logging.debug(msg=f"Arguments:\n{pformat(args)}")

    # Always create an output file to avoid bazel errors.
    args.output_file.touch()

    # Search for the .coverage file.
    coverage_file = list(Path(os.environ["RUNFILES_DIR"]).rglob("*.coverage"))

    if not coverage_file:
        return

    if len(coverage_file) > 1:
        logging.error("Found more than one .coverage file.")
        sys.exit(1)

    # Overwrite the empty output file with the found .coverage file.
    shutil.copy2(coverage_file[0], args.output_file)

    logging.info(f"Copied {coverage_file[0]} to {args.output_file}.")


def parse_args() -> argparse.Namespace:
    """Parse args."""

    parser = argparse.ArgumentParser()

    parser.add_argument("--coverage_dir", type=Path)
    parser.add_argument("--filter_sources", action="append")
    parser.add_argument("--output_file", type=Path)
    parser.add_argument("--source_file_manifest", type=Path)
    parser.add_argument("--sources_to_replace_file")

    return parser.parse_args()


if __name__ == "__main__":
    main()

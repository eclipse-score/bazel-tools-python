# *******************************************************************************
# Copyright (c) 2025 Contributors to the Eclipse Foundation
#
# See the NOTICE file(s) distributed with this work for additional
# information regarding copyright ownership.
#
# This program and the accompanying materials are made available under the
# terms of the Apache License Version 2.0 which is available at
# https://www.apache.org/licenses/LICENSE-2.0
#
# SPDX-License-Identifier: Apache-2.0
# *******************************************************************************

"""Custom coverage report generator for pycoverage."""

import argparse
import logging
import os
import shutil
import sys
from pathlib import Path
from pprint import pformat

from termcolor import colored


def main() -> int:
    """Main entry point."""
    logging.basicConfig(level=logging.INFO)
    logging.info(colored("Running output-generator on all executed tests", "magenta"))

    args = parse_args()
    logging.debug(msg=f"Arguments:\n{pformat(args)}")

    # Always create an output file to avoid bazel errors.
    args.output_file.touch()

    # Search for the .coverage file.
    coverage_file = list(Path(os.environ["RUNFILES_DIR"]).rglob("*.coverage"))

    if not coverage_file:
        return 0

    if len(coverage_file) > 1:
        logging.error("Found more than one .coverage file.")
        return 1

    # Overwrite the empty output file with the found .coverage file.
    shutil.copy2(coverage_file[0], args.output_file)

    logging.info(f"Copied {coverage_file[0]} to {args.output_file}.")

    return 0


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
    sys.exit(main())

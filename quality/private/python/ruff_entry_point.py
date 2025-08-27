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
"""Entry point for ruff python library.

This executes ruff as a subprocess by finding its binary, forwarding every
 argument and finally outputing its stdout, stderr and return code.
"""

import subprocess
import sys
from pathlib import Path

if __name__ == "__main__":
    from ruff import __main__ as ruff_main  # type: ignore[import-untyped]

    ruff_main_path = Path(ruff_main.__file__).resolve(strict=True)
    ruff_external = ruff_main_path.parent.parent.parent
    ruff_bin = ruff_external / "bin/ruff"
    result = subprocess.run([ruff_bin, *sys.argv[1:]], capture_output=True, text=True, check=False)
    sys.stdout.write(result.stdout)
    sys.stderr.write(result.stderr)
    sys.exit(result.returncode)

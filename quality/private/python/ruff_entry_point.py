"""Entry point for ruff python library.

This executes ruff as a subprocess by finding its binary, forwarding every
 argument and finally outputing its stdout, stderr and return code.
"""

import subprocess
import sys
from pathlib import Path

from ruff import __main__ as ruff_main  # type: ignore[import-untyped]

if __name__ == "__main__":
    ruff_main_path = Path(ruff_main.__file__).resolve(strict=True)
    ruff_external = ruff_main_path.parent.parent.parent
    ruff_bin = ruff_external / "bin/ruff"
    result = subprocess.run([ruff_bin, *sys.argv[1:]], capture_output=True, text=True, check=False)
    sys.stdout.write(result.stdout)
    sys.stderr.write(result.stderr)
    sys.exit(result.returncode)

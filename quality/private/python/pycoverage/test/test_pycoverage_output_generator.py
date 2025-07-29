# Copyright (C) 2025 Bayerische Motoren Werke Aktiengesellschaft (BMW AG). All rights reserved.

"""Tests for the pycoverage output_generator module."""

from pathlib import Path

import pytest

from quality.private.python.pycoverage import output_generator


@pytest.mark.parametrize(
    "coverage_files, output_file",
    [
        ([Path(".coverage")], Path("coverage.dat")),  # Happy path.
        ([], Path("coverage.dat")),  # Bad path: no coverage files found.
        (
            [Path("dir1/.coverage"), Path("dir2/.coverage")],
            Path("coverage.dat"),
        ),  # Bad path: More than one coverage files.
    ],
)
def test_pycoverage_merger_main(mocker, caplog, coverage_files, output_file):
    """Tests pycoverage output_generator main function."""
    mocker.patch("pathlib.Path.rglob", return_value=coverage_files)
    mocker.patch("pathlib.Path.touch", lambda self: None)
    mocker.patch("shutil.copy2", lambda *args, **kwargs: None)
    mocker.patch(
        "sys.argv",
        new=[
            "output_generator",
            "--output_file",
            str(output_file),
        ],
    )

    if len(coverage_files) > 1:
        assert output_generator.main() == 1
        assert "Found more than one .coverage file." in caplog.text
        return

    output_generator.main()

    if not coverage_files:
        return

    assert f"Copied {coverage_files[0]} to {output_file}." in caplog.text

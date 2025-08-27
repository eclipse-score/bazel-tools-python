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

"""Tests for the pycoverage report_generator module."""

from pathlib import Path

import pytest

from quality.private.python.pycoverage import report_generator


@pytest.mark.parametrize(
    "reports_file, st_size, output_file",
    [
        ("lcov_files.tmp", [1, 1, 1], Path(__file__)),  # Happy path.
        (
            "lcov_files_no_py_targets.tmp",
            [0, 1],
            Path(__file__),
        ),  # Bad path: no python targets.
        (
            "lcov_files.tmp",
            [1, 1, 1],
            Path("non_existing"),
        ),  # Bad path: output_file not generated.
    ],
)
def test_pycoverage_reporter_main(mocker, caplog, reports_file, st_size, output_file):
    """Tests pycoverage report_generator main function."""
    mocker.patch("pathlib.Path.touch", lambda self: None)
    # mock st_size
    mock_stat = mocker.Mock()
    mock_stat.st_size = st_size.pop(0)
    mocker.patch("pathlib.Path.stat", return_value=mock_stat)
    mocker.patch("coverage.Coverage.combine", lambda *args, **kwargs: None)
    mocker.patch("coverage.Coverage.save", lambda self: None)
    mocker.patch(
        "sys.argv",
        new=[
            "report_generator",
            "--output_file",
            str(output_file),
            "--reports_file",
            str(Path(__file__).parent / "data" / reports_file),
        ],
    )

    report_generator.main()

    if reports_file == "lcov_files_no_py_targets.tmp":
        assert "No python coverage reports found." in caplog.text
        return

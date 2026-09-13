"""Tests for PerceptGrid's entry point."""

import pytest

from perceptgrid.__main__ import main


def test_main_prints_project_status(capsys: pytest.CaptureFixture[str]) -> None:
    """The entry point prints the current project status."""
    main()

    captured = capsys.readouterr()

    assert captured.out == "PerceptGrid — project bootstrap in progress and testing.\n"

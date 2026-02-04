from pathlib import Path
from typing import Self
from unittest.mock import patch

import pytest


class TestFileLoader:
    argument_cases = [
        pytest.param("", 0, id="empty"),
        pytest.param(None, 0, id="None"),
        pytest.param(Path(), 1, id="valid path object"),
        pytest.param("abc", 3, id="string"),
    ]

    @pytest.mark.parametrize(("loader argument", "expected exception"), argument_cases)
    def test_handles_arguments_appropriately(
        self: Self, loader_arg, expected_exception
    ):
        if expected_exception is not None:
            with pytest.raises(expected_exception):
                loader = Loader(file=loader_arg)
        else:
            loader = Loader(file=loader_arg)

    def test_read_raw_content_success(self: Self, tmp_file: Path):
        with self._mock_path_state(exists=True, is_file=True):
            loader = Loader(file=tmp_file)
            loader.load_file(tmp_file)

            # If there's no exception, this test should pass.

    def test_read_raw_content_not_found(self: Self, tmp_file: Path):
        with self._mock_path_state(exists=False, is_file=True):
            loader = Loader(file=tmp_file)

            with pytest.raises(FileNotFoundError):
                loader.load_file(tmp_file)

    def test_read_raw_content_permission_denied(self: Self, tmp_file: Path):
        with self._mock_path_state(exists=True, is_file=True):
            tmp_file.chmod(0o000)
            loader = Loader(file=tmp_file)

            with pytest.raises(FileNotFoundError):
                loader.load_file(tmp_file)

    def test_read_raw_content_is_directory(self: Self, tmp_file: Path):
        with self.mock_path(exists=False, is_file=True):
            loader = Loader(file=tmp_file)

            with pytest.raises(IsADirectoryError):
                loader.load_file(tmp_file)

    def mock_path(self: Self, exists: bool, is_file: bool):
        return (
            patch.object(Path, "exists", return_value=exists),
            patch.object(Path, "is_file", return_value=is_file),
        )

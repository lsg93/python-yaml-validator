from contextlib import contextmanager
from pathlib import Path
from typing import Self
from unittest.mock import patch

import pytest

from src import FileLoader, InvalidArgumentException
from src.exceptions import LoaderFileNotFoundException


class TestFileLoader:
    argument_cases = [
        pytest.param(" ", InvalidArgumentException, id="empty"),
        pytest.param(None, InvalidArgumentException, id="None"),
        pytest.param(Path(), None, id="valid path object"),
        pytest.param("abc", None, id="string"),
    ]

    @pytest.mark.parametrize(("loader_argument", "expected_exception"), argument_cases)
    def test_handles_arguments_appropriately(
        self: Self, loader_argument, expected_exception
    ):
        if expected_exception is not None:
            with pytest.raises(expected_exception):
                _ = FileLoader(path=loader_argument)
        else:
            _ = FileLoader(path=loader_argument)

    def test_loads_file(self: Self):
        with self._mock_path(exists=True, is_file=True):
            loader = FileLoader(path="path/to/file.txt")
            _ = loader.load()

    def test_raises_exception_when_loading_nonexistent_file(self: Self):
        with self._mock_path(exists=False, is_file=True, has_permissions=True):
            with pytest.raises(LoaderFileNotFoundException):
                loader = FileLoader(path=Path("nonexistent/path/file.txt"))
                _ = loader.load()

    def test_raises_exception_when_loading_file_without_read_permissions(self: Self):
        with self._mock_path(exists=True, is_file=True, has_permissions=False):
            loader = FileLoader(path="protected/file.txt")

            with pytest.raises(PermissionError):
                _ = loader.load()

    def test_raises_exception_when_loading_file_which_is_directory(self: Self):
        with self._mock_path(exists=True, is_file=False):
            loader = FileLoader(path="/path/")

            with pytest.raises(IsADirectoryError):
                _ = loader.load()

    @contextmanager
    def _mock_path(
        self: Self,
        exists: bool,
        is_file: bool,
        has_permissions: bool = True,
    ):
        with (
            patch.object(Path, "exists", return_value=exists),
            patch.object(Path, "is_file", return_value=is_file),
            patch.object(Path, "is_dir", return_value=not is_file),
            patch("os.access", return_value=has_permissions),
        ):
            yield

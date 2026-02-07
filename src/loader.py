import os
from pathlib import Path
from typing import Self

from src.models import ConfigData, Loader

from .exceptions import InvalidArgumentException, LoaderFileNotFoundException


class FileLoader(Loader):
    def __init__(self: Self, path: Path | str):
        if path is None:
            raise InvalidArgumentException(
                "Path must be a string or an instance of a Path."
            )

        if isinstance(path, str):
            if len(path.strip()) > 0:
                self.path = Path(path)
            else:
                raise InvalidArgumentException(
                    "An empty string cannot be supplied as an argument."
                )
        else:
            self.path = path

    def load(self):
        if self.path.is_dir():
            raise IsADirectoryError

        if not os.access(self.path, os.R_OK):
            raise PermissionError(f"Cannot read file at {self.path}")

        if self.path.exists() and self.path.is_file():
            return ConfigData(data=self.path.read_text(), format=self.path.suffix)
        else:
            raise LoaderFileNotFoundException

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


class ConfigFileNotFoundException(Exception):
    pass


class NoDefaultConfigException(Exception):
    def __str__(self):
        return "Default config file not found in root folder."


class InvalidArgumentException(Exception):
    pass


# This class hasn't got any actual usage at the moment, it's just a foundation to get tests passing.
@dataclass
class Config:
    path: Optional[str] = None

    def load_from_file(self, path: Optional[Path] = None):
        if self.path is None:
            path = Path(os.getenv("DEFAULT_CONFIG_PATH"))

        if path.exists() and path.is_file():
            return path
        else:
            if self.path is None:
                raise NoDefaultConfigException
            else:
                raise ConfigFileNotFoundException

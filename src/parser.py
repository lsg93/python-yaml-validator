from typing import Protocol, Self

import yaml
from yaml.parser import ParserError
from yaml.scanner import ScannerError

from src.exceptions import EmptySourceException, YAMLException
from src.models import ConfigData, Parser


class YAMLWrapper(Protocol):
    """A simple abstraction for whichever library we use to read YAML"""

    def load(self: Self, str: str): ...


class PYYAMLWrapper(YAMLWrapper):
    def load(self, str: str):
        try:
            return next(yaml.safe_load_all(stream=str))

        # If we yield on an empty file, this will be raised.
        except StopIteration:
            raise EmptySourceException
        except (ParserError, ScannerError) as e:
            raise YAMLException("The provided YAML is invalid.") from e
        except Exception as e:
            raise e


class YAMLParser(Parser):
    def __init__(self: Self, wrapper: YAMLWrapper):
        self.supported_formats = ("yaml", "yml")
        self.wrapper = wrapper

    def parse(self: Self, source: ConfigData) -> dict:
        result = self.wrapper.load(source.data())

        # Check dictionary is empty before returning, otherwise throw specific exception.
        if result is None:
            raise EmptySourceException

        source.rules = result

        return result

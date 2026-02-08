from typing import Protocol, Self

import yaml

from src.models import ConfigData, Parser


class YAMLWrapper(Protocol):
    """A simple abstraction for whichever underlying library we use to read yaml"""

    def load(self: Self, str: str): ...


class PYYamlWrapper(YAMLWrapper):
    def load(self, str: str):
        return yaml.safe_load(stream=str)


class YAMLParser(Parser):
    def __init__(self: Self, wrapper: YAMLWrapper):
        self.supported_formats = ("yaml", "yml")
        self.wrapper = wrapper

    def parse(self: Self, source: ConfigData) -> dict:
        try:
            source.rules = self.wrapper.load(source.data())
        except Exception as e:
            raise e

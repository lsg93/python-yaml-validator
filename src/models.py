from dataclasses import dataclass
from typing import Protocol


@dataclass
class ConfigData:
    data: str
    format: str


class Loader(Protocol):
    def load() -> ConfigData: ...


class Parser(Protocol):
    supported_formats: list[str]

    def parse(data: ConfigData) -> Rules: ...


class Rules(object): ...

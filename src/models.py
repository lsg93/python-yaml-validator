from dataclasses import dataclass
from typing import Callable, Protocol, Self


@dataclass
class ConfigData:
    data: Callable[[], str]
    format: str
    rules: None | dict = None


class Loader(Protocol):
    def load(self: Self) -> ConfigData: ...


class Parser(Protocol):
    supported_formats: list[str]

    def parse(data: ConfigData) -> dict: ...


class Rules(object): ...

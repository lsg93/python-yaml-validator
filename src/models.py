from dataclasses import dataclass, field
from typing import Callable, Protocol, Self


@dataclass
class ConfigData:
    data: Callable[[], str]
    format: str
    rules: dict = field(default_factory=dict)


class Loader(Protocol):
    def load(self: Self) -> ConfigData: ...


class Parser(Protocol):
    supported_formats: list[str]

    def parse(data: ConfigData) -> dict: ...


class Rules(object): ...

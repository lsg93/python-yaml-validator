from dataclasses import dataclass
from typing import Any, Callable, Protocol, Self, runtime_checkable


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


@runtime_checkable
class RuleProtocol(Protocol):
    message: str

    def __call__(self: Self, attribute: Any) -> bool: ...

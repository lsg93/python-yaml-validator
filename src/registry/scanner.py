import importlib
import importlib.metadata
import importlib.util
from pathlib import Path
from typing import Iterator, Protocol, runtime_checkable

from src.models import RuleProtocol

DEFAULT_PATH = Path(__file__).parent.parent / "rules"


@runtime_checkable
class RuleLoader(Protocol):
    _identifier: str

    def getIdentifier(self) -> str: ...

    def load(self) -> RuleProtocol: ...


class InternalRuleLoader(Protocol):
    def __init__(self, path: Path):
        self.path = path

    # TODO - read about importlib.util.spec_from_file_location
    def load(self):
        spec = importlib.util.spec_from_file_location(self.path)


class ExternalRuleLoader(Protocol):
    def __init__(self, entry_point: importlib.metadata.EntryPoint):
        self.entry_point = entry_point

    def load(self):
        self.entry_point.load()


class Scanner(object):
    def __init__(
        self,
    ):
        self.internal_root = DEFAULT_PATH

    def get_rules(self) -> Iterator[RuleLoader]:
        yield from self._scan_internal_rules()
        yield from self._scan_external_rules()

    def _scan_internal_rules(self) -> Iterator[InternalRuleLoader]:
        path = Path(DEFAULT_PATH)
        for file in path.rglob("*_rule.py"):
            if file.is_file():
                yield InternalRuleLoader(path=file)

    def _scan_external_rules(self) -> Iterator[ExternalRuleLoader]:
        entry_points = importlib.metadata.entry_points(
            group="python-yaml-validator.extra-rules"
        )

        for entry_point in entry_points:
            yield ExternalRuleLoader(entry_point=entry_point)

import importlib
import importlib.metadata
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

DEFAULT_PATH = Path(__file__).parent.parent / "rules"


@dataclass
class InternalRule:
    path: Path

    # TODO - read about importlib.util.spec_from_file_location
    def load(): ...


@dataclass
class ExternalRule:
    entry_point: importlib.metadata.EntryPoint

    def load(self):
        self.entry_point.load()


class Scanner(object):
    def __init__(
        self,
    ):
        self.internal_root = DEFAULT_PATH

    def get_rules(self):
        yield from self._scan_internal_rules()
        yield from self._scan_external_rules()

    def _scan_internal_rules(self) -> Iterator[InternalRule]:
        path = Path(DEFAULT_PATH)
        for file in path.rglob("*_rule.py"):
            if file.is_file():
                yield InternalRule(path=file)

    def _scan_external_rules(self) -> Iterator[ExternalRule]:
        entry_points = importlib.metadata.entry_points(
            group="python-yaml-validator.extra-rules"
        )

        for entry_point in entry_points:
            yield ExternalRule(entry_point=entry_point)

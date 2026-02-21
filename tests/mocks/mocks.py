from dataclasses import dataclass


@dataclass
class MockLoader:
    valid: bool
    calls: int = 0
    _identifier: str = ""

    def getIdentifier(self) -> str:
        return self._identifier


@dataclass
class ValidLoader(MockLoader):
    def load(self):
        self.calls += 1


@dataclass
class InvalidLoader(MockLoader): ...

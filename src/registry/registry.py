from typing import Iterable, Self

from src.registry.scanner import RuleLoader


class RuleRegistry:
    def __init__(self: Self, rules: Iterable[RuleLoader]):
        self.rules = list()

        for rule in rules:
            self.rules.append(rule)

    def __len__(self: Self):
        return len(self.rules)

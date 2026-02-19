from typing import Iterable, Self

from src.registry.scanner import RuleLoader


class NoValidRulesInRegistryException(Exception): ...


class InvalidRuleLoaderException(Exception): ...


class RuleRegistry:
    def __init__(self: Self, rules: Iterable[RuleLoader]):
        self.rules = dict()
        self.errors = list()

        for rule in rules:
            if isinstance(rule, RuleLoader) is False:
                self.errors.append(InvalidRuleLoaderException("Invalid rule."))
                continue

            identifier = rule.getIdentifier()

            if identifier in self.rules:
                self.errors.append(
                    InvalidRuleLoaderException(
                        "Rule with this identifier already exists in registry."
                    )
                )
                continue

            self.rules[rule.getIdentifier()] = rule

        if len(self) == 0:
            raise NoValidRulesInRegistryException(
                "No valid rules exist in the registry."
            )

    def __len__(self: Self):
        return len(self.rules)

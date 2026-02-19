from collections import namedtuple
from typing import List, NamedTuple

import pytest

# Why do imports not work as expected?
from src.registry.registry import (
    InvalidRuleLoaderException,
    NoValidRulesInRegistryException,
    RuleRegistry,
)
from src.registry.scanner import RuleLoader


class MockInternalRuleLoader(RuleLoader):
    def __init__(self):
        self.calls = 0
        self._identifier = "internal_rule"

    def getIdentifier(self) -> str:
        return self._identifier

    def load(self):
        self.calls + 1


class MockExternalRuleLoader(RuleLoader):
    def __init__(self):
        self.calls = 0
        self._identifier = "external_rule"

    def getIdentifier(self) -> str:
        return self._identifier

    def load(self):
        self.calls += 1


class MockInvalidRuleLoader:
    def __init__(self):
        self.calls = 0

    def load(self):
        self.calls += 1


class TestRuleRegistry:
    @pytest.fixture()
    def mocked_rules(self) -> NamedTuple:
        Mocks = namedtuple(
            "Mocks", ["valid_internal_rule", "valid_external_rule", "invalid_rule"]
        )

        return Mocks(
            MockInternalRuleLoader(), MockExternalRuleLoader(), MockInvalidRuleLoader()
        )

    def test_registry_stores_given_rules_(self, mocked_rules):
        valid_internal_rule, valid_external_rule, _ = mocked_rules
        rules = [valid_internal_rule, valid_external_rule]

        registry = RuleRegistry(rules=iter(rules))

        assert len(registry) == len(list(rules))
        assert len(registry.errors) == 0
        self.assertRulesNotCalledByRegistry(rules)

    def test_registry_stores_exception_if_a_given_rule_is_invalid(self, mocked_rules):
        valid_internal_rule, _, invalid_rule = mocked_rules
        rules = [valid_internal_rule, invalid_rule]
        registry = RuleRegistry(rules=iter(rules))

        assert len(registry) == len(rules) - 1
        self.assertRulesNotCalledByRegistry(rules)
        assert len(registry.errors) == 1

        expected_exception = registry.errors[0]
        assert isinstance(expected_exception, InvalidRuleLoaderException)

        assert "Invalid rule" in str(expected_exception)

    def test_registry_stores_exception_if_given_rules_contain_duplicates(
        self, mocked_rules
    ):
        valid_internal_rule, _, _ = mocked_rules
        rules = [valid_internal_rule, valid_internal_rule]
        registry = RuleRegistry(rules=iter(rules))

        assert len(registry) == len(rules) - 1
        assert len(registry.errors) == 1

        expected_exception = registry.errors[0]
        assert isinstance(expected_exception, InvalidRuleLoaderException)

        assert "identifier already exists" in str(expected_exception)

    def test_registry_throws_exception_if_no_rules_can_be_stored(self, mocked_rules):
        _, _, invalid_rule = mocked_rules
        rules = [invalid_rule]

        with pytest.raises(NoValidRulesInRegistryException):
            _ = RuleRegistry(rules=iter(rules))

    def assertRulesNotCalledByRegistry(self, rules: List[RuleLoader]):
        for rule in rules:
            assert rule.calls == 0

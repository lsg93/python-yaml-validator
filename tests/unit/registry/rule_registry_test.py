from typing import List

import pytest

# Why do imports not work as expected?
from src.registry.registry import (
    InvalidRuleLoaderException,
    NoValidRulesInRegistryException,
    RuleRegistry,
)
from src.registry.scanner import RuleLoader
from tests.mocks.mocks import InvalidLoader, MockLoader, ValidLoader


class TestRuleRegistry:
    @pytest.fixture()
    def mock_rules(self) -> List[MockLoader]:
        def setup_mocks(mock_list: List[dict]):
            def return_loader(arguments):
                return (
                    ValidLoader(**arguments)
                    if arguments["valid"]
                    else InvalidLoader(**arguments)
                )

            return [return_loader(arguments) for arguments in mock_list]

        return setup_mocks

    def test_registry_stores_given_rules_(self, mock_rules):
        rules = mock_rules(
            [
                {"_identifier": "rule_one", "valid": True},
                {"_identifier": "rule_two", "valid": True},
            ]
        )

        registry = RuleRegistry(rules=iter(rules))

        assert len(registry) == len(list(rules))
        assert len(registry.errors) == 0
        self.assertRulesNotCalledByRegistry(rules)

    def test_registry_stores_exception_if_a_given_rule_is_invalid(self, mock_rules):
        rules = mock_rules(
            [
                {"_identifier": "rule_one", "valid": True},
                {"_identifier": "rule_two", "valid": False},
            ]
        )
        registry = RuleRegistry(rules=iter(rules))

        assert len(registry) == len(rules) - 1
        self.assertRulesNotCalledByRegistry(rules)
        assert len(registry.errors) == 1

        expected_exception = registry.errors[0]
        assert isinstance(expected_exception, InvalidRuleLoaderException)

        assert "Invalid rule" in str(expected_exception)

    def test_registry_stores_exception_if_given_rules_contain_duplicates(
        self, mock_rules
    ):
        rules = mock_rules(
            [
                {"_identifier": "rule_one", "valid": True},
                {"_identifier": "rule_one", "valid": True},
            ]
        )

        registry = RuleRegistry(rules=iter(rules))

        assert len(registry) == len(rules) - 1
        assert len(registry.errors) == 1

        expected_exception = registry.errors[0]
        assert isinstance(expected_exception, InvalidRuleLoaderException)

        assert "identifier already exists" in str(expected_exception)

    def test_registry_throws_exception_if_no_rules_can_be_stored(self, mock_rules):
        rules = mock_rules([])

        with pytest.raises(NoValidRulesInRegistryException):
            _ = RuleRegistry(rules=iter(rules))

    def assertRulesNotCalledByRegistry(self, rules: List[RuleLoader]):
        for rule in rules:
            assert rule.calls == 0

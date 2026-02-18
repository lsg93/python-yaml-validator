from collections import namedtuple
from typing import NamedTuple

import pytest

# Why do imports not work as expected?
from src.models import RuleProtocol
from src.registry.registry import RuleRegistry


class MockInternalRuleLoader(RuleProtocol):
    def __init__(self):
        pass

    def load(): ...


class MockExternalRuleLoader(RuleProtocol):
    def __init__(self):
        pass

    def load(): ...


class MockInvalidRuleLoader(RuleProtocol):
    def __init__(self):
        pass

    def load(): ...


class TestRuleRegistry:
    @pytest.fixture()
    def mocked_rules() -> NamedTuple:
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

    def test_registry_stores_exception_if_a_given_rule_is_invalid(self, mocked_rules):
        valid_internal_rule, _, invalid_rule = mocked_rules
        rules = [valid_internal_rule, invalid_rule]
        registry = RuleRegistry(rules=iter(rules))

        assert len(registry) == (len(list(rules) - 1))
        assert len(registry.errors) == 1
        assert isinstance(registry.errors[0]["exception"], InvalidRuleException)

    def test_registry_stores_exception_if_given_rules_contain_duplicates(
        self, mocked_rules
    ):
        valid_internal_rule, _, _ = mocked_rules
        rules = [valid_internal_rule, valid_internal_rule]
        registry = RuleRegistry(rules=iter(rules))

        assert len(registry) == (len(list(rules) - 1))
        assert len(registry.errors) == 1
        assert isinstance(registry.errors[0]["exception"], DuplicateRuleNameException)

    def test_registry_throws_exception_if_no_rules_can_be_stored(self, mocked_rules):
        valid_internal_rule, _, invalid_rule = mocked_rules
        rules = [valid_internal_rule, invalid_rule]

        with pytest.raises(NoRulesFoundException):
            registry = RuleRegistry(rules=iter(rules))

        assert len(registry) == 0
        assert len(registry.errors) == 1
        assert isinstance(registry.errors[0]["exception"], NoRulesFoundException)

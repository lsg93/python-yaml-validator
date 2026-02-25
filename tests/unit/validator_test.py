from dataclasses import dataclass
from unittest.mock import MagicMock

import pytest

from src.validator import Validator
from tests.mocks.mocks import MockLoader


@dataclass
class ValidatorMockLoader(MockLoader):
    return_value: bool = True

    def load(self, **params): ...


class TestValidator:
    @pytest.fixture()
    def setup_mocks(self):
        def add_mocks_to_loaders(rules: dict):
            """This function adds a pass/fail mocked load method based on the "valid" argument
            We will use the mocks to make assertions in our tests.
            """
            for rule in rules.values():
                if rule.valid is True:
                    rule.load = MagicMock(return_value=rule.return_value)
                else:
                    rule.load = MagicMock(side_effect=Exception)

            return rules

        return add_mocks_to_loaders

    def test_validator_calls_correct_rule_from_registry_based_on_attribute(
        self, setup_mocks
    ):
        config = {"memory_limit": {"rule": "numeric"}}
        data = {"memory_limit": 512}
        rules = setup_mocks(
            {"numeric": ValidatorMockLoader(valid=True, _identifier="numeric")}
        )

        validator = Validator(config=config, data=data, rules=rules)
        validator.validate()

        rules["numeric"].load.assert_called_once()

    def test_validator_can_call_multiple_rules(self, setup_mocks):
        config = {"memory_limit": {"rule": "numeric"}}
        data = {"memory_limit": 512}
        rules = setup_mocks(
            {"numeric": ValidatorMockLoader(valid=True, _identifier="numeric")}
        )

        validator = Validator(config=config, data=data, rules=rules)
        validator.validate()

        rules["numeric"].load.assert_called_once()

    attribute_path_cases = (
        pytest.param(id="top level rule"),
        pytest.param(id="nested rule"),
    )

    # Test normal and nested route here
    def test_validator_provides_path_to_attribute_if_validation_fails(
        self, setup_mocks
    ):
        config = {"memory_limit": {"rule": "numeric"}}
        data = {"memory_limit": "abc"}
        rules = setup_mocks(
            {
                "numeric": ValidatorMockLoader(
                    valid=True, return_value=False, _identifier="numeric"
                )
            }
        )

        validator = Validator(config=config, data=data, rules=rules)
        validator.validate()

        rules["numeric"].load.assert_called_once()
        assert "numeric" in validator.failures

    def test_validator_calls_rules_with_params_if_provided(self, setup_mocks):
        config = {
            "database": {
                "engine": {
                    "rule": "choice",
                    "params": {"choices": ["mysql", "postgresql"]},
                }
            },
        }

        data = {"database": {"engine": "mysql"}}

        rules = setup_mocks(
            {"choice": ValidatorMockLoader(valid=True, _identifier="choice")}
        )

        validator = Validator(config=config, data=data, rules=rules)
        validator.validate()

    def test_validator_calls_correct_rule_when_attributes_are_nested(self, setup_mocks):
        config = {
            "load_balancer": {
                "protocol": {
                    "rule": "choice",
                    "params": {"options": ["HTTP", "HTTPS"]},
                    "port": {
                        "rule": "range",
                        "params": {"min": 1024, "max": 65535},
                    },
                },
            },
        }

        data = {"load_balancer": {"protocol": "HTTP", "port": 8080}}

        rules = setup_mocks(
            {
                "choice": ValidatorMockLoader(valid=True, _identifier="choice"),
                "range": ValidatorMockLoader(valid=True, _identifier="range"),
            }
        )

        validator = Validator(config=config, data=data, rules=rules)
        validator.validate()

    def test_validator_raises_exception_when_building_targets_if_data_is_malformed():
        pass

    def test_validator_raises_exception_if_a_given_rule_cannot_be_found():
        config = {"memory_limit": {"rule": "numeric"}}
        data = {"memory_limit": 512}
        rules = {"numeric": ValidatorMockLoader(valid=True, _identifier="numeric")}

        with pytest.raises(RuleNotFoundException, match='"numeric" not found'):
            Validator(config=config, data=data, rules=rules)

    def test_validator_catches_exceptions_thrown_by_rules():
        config = {"memory_limit": {"rule": "numeric"}}
        data = {"memory_limit": 512}
        rules = {"numeric": InvalidLoader(valid=True, _identifier="numeric")}

        with pytest.raises(ValidatorException) as exception:
            # Assert that the exception extends from the exception thrown by InvalidLoader!
            Validator(config=config, data=data, rules=rules)

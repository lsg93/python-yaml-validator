from unittest.mock import MagicMock

import pytest

from src.validator import Validator
from tests.mocks.mocks import InvalidLoader, ValidLoader
from tests.unit.registry.rule_registry_test import MockLoader


class ValidatorMockLoader(MockLoader):
    def load(self): ...


class TestValidator:
    @pytest.fixture()
    def setup_mocks(self):
        def add_mocks_to_loaders(rules: dict):
            """This function adds a pass/fail mocked load method based on the "valid" argument
            We will use the mocks to make assertions in our tests.
            """
            for rule in rules.values():
                if rule.valid is True:
                    rule.load = MagicMock(return_value=True)
                else:
                    rule.load = MagicMock(side_effect=Exception)

            return rules

        return add_mocks_to_loaders

    def test_validator_calls_correct_rule_from_registry_based_on_attribute(
        self, setup_mocks
    ):
        config = {"memory_limit": {"rule": "numeric"}}
        data = {"memory_limit": 512}
        rules = setup_mocks({"numeric": MockLoader(valid=True, _identifier="numeric")})

        validator = Validator(config=config, data=data, rules=rules)
        validator.validate()

        rules["numeric"].load.assert_called_once()

    def test_validator_provides_path_to_attribute_if_validation_fails():
        config = {"memory_limit": {"rule": "numeric"}}
        data = {"memory_limit": "abc"}
        rules = {"numeric": MockLoader(valid=True, _identifier="numeric")}

    def test_validator_calls_rules_with_params_if_provided():
        config = {
            "database": {
                "engine": {
                    "rule": "choice",
                    "params": {"choices": ["mysql", "postgresql"]},
                }
            },
        }

        data = {"database": {"engine": "mysql"}}

        rules = {"choice": ValidLoader(valid=True, _identifier="choice")}

        validator = Validator(data=data, rules=rules)
        validator.validate()

        assert ValidLoader.called_with == 512
        assert ValidLoader.calls == 1

    def test_validator_calls_correct_rule_when_attributes_are_nested():
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

        rules = {
            "choice": ValidLoader(valid=True, _identifier="choice"),
            "range": ValidLoader(valid=True, _identifier="range"),
        }

        validator = Validator(config=config, data=data, rules=rules)

        assert ValidLoader.called_with == 512
        assert ValidLoader.calls == 1

    def test_validator_raises_exception_if_a_given_rule_cannot_be_found():
        config = {"memory_limit": {"rule": "numeric"}}
        data = {"memory_limit": 512}
        rules = {"numeric": MockLoader(valid=True, _identifier="numeric")}

        with pytest.raises(RuleNotFoundException, match='"numeric" not found'):
            Validator(config=config, data=data, rules=rules)

    def test_validator_catches_exceptions_thrown_by_rules():
        config = {"memory_limit": {"rule": "numeric"}}
        data = {"memory_limit": 512}
        rules = {"numeric": InvalidLoader(valid=True, _identifier="numeric")}

        with pytest.raises(ValidatorException) as exception:
            # Assert that the exception extends from the exception thrown by InvalidLoader!
            Validator(config=config, data=data, rules=rules)

from typing import Iterable

from src.registry.scanner import RuleLoader


class RuleNotFoundException(Exception):
    pass


class RuleException(Exception):
    pass


class Validator:
    def __init__(self, config: dict, data: dict, rules: Iterable[RuleLoader]):
        self.config = config
        self.rules = rules
        self.results = dict()

    def validate(self) -> bool:
        for attribute, rule_definition in self.config.items():
            try:
                value = self._get_attribute_value(attribute)
                self.results[attribute] = self._validate_value(
                    value=value,
                    rule=rule_definition["rule"],
                    params=rule_definition["params"],
                )
            except Exception:
                # Not sure what to do here...
                pass

    def _get_attribute_value(self, attribute: str):
        # This is where we need to do a walk
        value = self.data.get(attribute)
        if value is None:
            raise RuleNotFoundException(f'Rule "{attribute}" not found.')
        return value

    def _validate_value(self, value: any, rule: RuleLoader, params: any):
        try:
            callable_rule = rule.load()
            return callable_rule(value, **params)
        except Exception as caught_exception:
            # We can't always know what exception is being thrown, so we just re-raise it as something more user friendly.
            raise RuleException from caught_exception

from typing import Iterable, Optional

from src.registry.scanner import RuleLoader


class ValueNotFoundException(Exception):
    pass


class RuleNotFoundException(Exception):
    pass


class RuleException(Exception):
    pass


class Validator:
    # config needs to be a named tuple maybe for better typing?
    def __init__(self, config: dict, data: dict, rules: Iterable[RuleLoader]):
        self.config = config
        self.data = data
        self.rules = rules
        self.results = dict()

    def validate(self) -> bool:
        for attribute, rule_definition in self.config.items():
            try:
                value = self._get_attribute_value(attribute)
                rule = self._get_rule(rule_definition["rule"])
                self.results[attribute] = self._validate_value(
                    value=value,
                    rule=rule,
                    params=rule_definition.get("params"),
                )
            except Exception:
                # Not sure what to do here...
                pass

    def _get_attribute_value(self, attribute: str):
        # This is where we need to do a walk
        value = self.data.get(attribute)
        if value is None:
            raise RuleNotFoundException(f'Value for "{attribute}" not found.')
        return value

    def _get_rule(self, name: str) -> RuleLoader:
        rule = self.rules.get(name)
        if rule is None:
            raise RuleNotFoundException(f'Rule "{rule}" not found.')
        return rule

    def _validate_value(
        self, value: any, rule: RuleLoader, params: Optional[dict] = {}
    ):
        try:
            callable_rule = rule.load()
            return callable_rule(value, **params)
        except Exception as caught_exception:
            # We can't always know what exception is being thrown, so we just re-raise it as something more user friendly.
            raise RuleException from caught_exception

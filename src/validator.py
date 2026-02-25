from typing import ItemsView, Iterable, List, Optional

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
        self.results = {}
        self.failures = {}

    def validate(self) -> bool:
        validation_targets = self._build_validation_targets(self.config.items())

        for attribute, value in validation_targets:
            try:
                value, rule = self._get_attribute(attribute)
                passed = self._validate_value(value=value, rule=rule)
                self.results[attribute] = passed

                if not passed:
                    self.failures[attribute] = rule.message

            except Exception:
                # Not sure what to do here...
                pass

    def _build_validation_targets(
        self,
        items: ItemsView,
        path: Optional[List[str]] = None,
        targets: Optional[dict] = None,
    ):
        """Loop through given object, looking for "rule" instances"""

        if path is None:
            path = []
        if targets is None:
            targets = {}

        for attribute, rule_definition in items:
            if isinstance(rule_definition, dict) and attribute != "params":
                path.append(attribute)
                self._build_validation_targets(rule_definition.items(), path, targets)
                # Remove key from path after recursion
                path.pop()
            else:
                resolved_path = ".".join(path)

                # Use dict.setdefault() to prevent issues with key orders
                if attribute in ("params", "rule"):
                    targets.setdefault(resolved_path, {})[attribute] = rule_definition
                else:
                    self._build_validation_targets(
                        rule_definition.items(), [resolved_path], targets
                    )

        return targets

    # def _get_attribute(self, attribute: str): NamedTuple
    #     # This is where we need to do a walk
    #     value = self.data.get(attribute)
    #     if value is None:
    #         raise RuleNotFoundException(f'Value for "{attribute}" not found.')
    #     return value

    # def _get_rule(self, name: str) -> RuleLoader:
    #     rule = self.rules.get(name)
    #     if rule is None:
    #         raise RuleNotFoundException(f'Rule "{rule}" not found.')
    #     return rule

    # def _validate_value(
    #     self, value: any, rule: RuleLoader, params: Optional[dict] = {}
    # ):
    #     try:
    #         callable_rule = rule.load()
    #         return callable_rule(value, **params)
    #     except Exception as caught_exception:
    #         # We can't always know what exception is being thrown, so we just re-raise it as something more user friendly.
    #         raise RuleException from caught_exception

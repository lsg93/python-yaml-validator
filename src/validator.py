from typing import ItemsView, Iterable, List, Optional

from src.registry.scanner import RuleLoader


class AttributeNotFoundException(Exception): ...


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

        for attribute, rule_definition in validation_targets.items():
            try:
                value = self._get_attribute(attribute)
                rule = self._get_rule(rule_definition["rule"])
                params = rule_definition.get("params", {})

                passed = self._validate_value(value=value, rule=rule, **params)
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

    def _get_attribute(self, attribute: str):
        # Given attributes can be nested with dot notation,
        # So we need to use this dot notation to traverse the data dictionary.
        # And get the right value for the given attribute.

        path = attribute.split(".")
        current = self.data

        for property in path:
            if not isinstance(current, dict):
                raise AttributeNotFoundException(
                    f'Could not find attribute "{property}" in given data.'
                )

            value = current.get(property)

            if value is None:
                raise AttributeNotFoundException(
                    f'Could not find attribute "{property}" in given data.'
                )

            current = value

        return current

    def _get_rule(self, identifier: str, **params) -> RuleLoader:
        rule = self.rules.get(identifier)

        if rule is None:
            raise RuleNotFoundException(f'Rule "{rule}" not found.')
        return rule

    def _validate_value(self, value: any, rule: RuleLoader, **params):
        try:
            callable_rule = rule.load()
            return callable_rule(value, **params)
        except Exception as caught_exception:
            # We can't always know what exception is being thrown here, so we just re-raise it as something more user friendly.
            raise RuleException from caught_exception

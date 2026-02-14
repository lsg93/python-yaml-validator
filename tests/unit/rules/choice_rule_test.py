from typing import Self

from src.models import RuleProtocol
from src.rules.choice import ChoiceRule


class TestChoiceRule:
    def test_rule_implements_protocol_correctly(self: Self):
        rule = ChoiceRule(("a", "b", "c"))

        assert callable(rule) is True
        assert isinstance(rule, RuleProtocol)

    def test_rule_validates_against_choices(self: Self):
        rule = ChoiceRule(("a", "b", "c"))
        assert rule("a") is True

    def test_rule_fails_for_invalid_choice(self: Self):
        rule = ChoiceRule(("a", "b", "c"))
        assert rule("d") is False

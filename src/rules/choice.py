from src.exceptions import InvalidArgumentException
from src.models import RuleProtocol


class ChoiceRule(RuleProtocol):
    def __init__(self, choices: list[str]):
        if not choices:
            raise InvalidArgumentException("No possible choices were given.")

        self.message = ""
        # convert list to set for lookup?
        self.choices = set(choices)

    def __call__(self, attribute: str) -> bool:
        if attribute not in self.choices:
            self.message = f"Given value {attribute} is not present in {self.choices}"
            return False

        return True

from typing import Callable, Self

import pytest
from stubs import valid_yaml_stub

from src.models import ConfigData
from src.parser import PYYamlWrapper, YAMLParser

# Code

type ConfigDataFactory = Callable[[str], ConfigData]


class TestYamlParser:
    @pytest.fixture()
    def yaml_data(self: Self) -> ConfigDataFactory:
        def setup_config_data(yaml: str) -> ConfigDataFactory:
            return ConfigData(data=lambda: yaml, format="yaml")

        return setup_config_data

    def test_parser_successfully_parses_valid_yaml(self, yaml_data: ConfigDataFactory):
        data = yaml_data(valid_yaml_stub["input"])
        expected_result = valid_yaml_stub["expected_result"]
        parser = YAMLParser(wrapper=PYYamlWrapper())
        parser.parse(data)

        assert data.rules == expected_result

    # def test_parser_raises_exception_if_yaml_is_malformed(self):
    #     pass

    # def test_parser_raises_exception_if_yaml_is_empty(self):
    #     pass

    # def test_parser_handles_incorrect_nesting(self):
    #     pass

    # def test_parser_handles_multiple_inline_documents(self):
    #     pass

    pass

from typing import Callable, Self

import pytest
from stubs.test_parser_stubs import (
    empty_yaml_stub,
    incorrectly_nested_yaml_stub,
    malformed_yaml_stub,
    multiple_documents_yaml_stub,
    valid_yaml_stub,
)

from src.exceptions import EmptySourceException, YAMLException
from src.models import ConfigData
from src.parser import PYYAMLWrapper, YAMLParser

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

        parser = YAMLParser(wrapper=PYYAMLWrapper())
        parser.parse(data)

        assert data.rules == expected_result

    parser_exception_cases = [
        pytest.param(malformed_yaml_stub["input"], id="malformed yaml"),
        pytest.param(
            incorrectly_nested_yaml_stub["input"],
            id="incorrectly nested yaml",
        ),
    ]

    @pytest.mark.parametrize(("input"), parser_exception_cases)
    def test_parser_raises_exception(
        self,
        yaml_data: ConfigDataFactory,
        input: str,
    ):
        data = yaml_data(input)
        parser = YAMLParser(wrapper=PYYAMLWrapper())

        with pytest.raises(YAMLException):
            parser.parse(data)

    def test_parser_raises_exception_for_empty_yaml(self, yaml_data: ConfigDataFactory):
        data = yaml_data(empty_yaml_stub["input"])
        parser = YAMLParser(wrapper=PYYAMLWrapper())

        with pytest.raises(EmptySourceException):
            parser.parse(data)
            assert data.rules is None

    """" Even though it's not realistically going to happen, 
        this is a decent test to have 
        in case we actually do want this functionality later """

    def test_parser_parses_ignores_multiple_inline_documents(
        self, yaml_data: ConfigDataFactory
    ):
        data = yaml_data(multiple_documents_yaml_stub["input"])
        expected_result = multiple_documents_yaml_stub["expected_result"]

        parser = YAMLParser(wrapper=PYYAMLWrapper())
        parser.parse(data)

        assert data.rules == expected_result

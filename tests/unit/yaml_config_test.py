from contextlib import nullcontext
from dataclasses import dataclass, field

import pytest

from src import Config, ConfigData, InvalidConfigFileExtensionException


class TestConfigWithYamlParser:
    # Parameterising this test in case future updates require different extensions.
    extension_cases = [
        pytest.param("YAML", None, id="uppercased extension"),
        pytest.param(".yml", None, id="period in extension"),
        pytest.param(".txt", True, id="invalid extension"),
        pytest.param("", True, id="no extension"),
    ]

    @pytest.mark.parametrize(("given_extension", "raises_exception"), extension_cases)
    def test_config_raises_exception_for_invalid_file_extensions(
        self,
        given_extension: str,
        raises_exception: bool,
    ):
        data = ConfigData(data="test", format=given_extension)
        mock_parser = MockYamlParser(supported_formats=("yaml", "yml"))

        with (
            pytest.raises(InvalidConfigFileExtensionException)
            if raises_exception is True
            else nullcontext()
        ):
            _ = Config(
                source=data,
                parser=mock_parser,
            )

        if raises_exception is not True:
            assert mock_parser.call_count == 1

    def test_config_returns_parsed_rules_as_property(self):
        data = ConfigData(data="test", format="yaml")
        mock_parser = MockYamlParser(supported_formats=("yaml", "yml"))

        _ = Config(source=data, parser=mock_parser)

        assert mock_parser.call_count == 1


@dataclass
class MockYamlParser:
    call_count: int = 0
    supported_formats: list = field(default_factory=list)

    def parse(self, _: ConfigData):
        self.call_count += 1
        return Rules()

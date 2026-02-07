from contextlib import nullcontext
from typing import List, Optional

import pytest

# TODO - clean up parameterisation
# TODO - don't try and mock - use a fake class in this test instead.


class TestConfig:
    # Parameterising this test in case future updates require different extensions.
    extension_cases = [
        pytest.param(
            ("yaml", "yml"),
            ("yaml", "yml", ".yaml", ".yml", "YML", "YAML", ".txt", ""),
            (
                None,
                None,
                None,
                None,
                None,
                None,
                InvalidConfigFileExtensionException,
                InvalidConfigFileExtensionException,
            ),
            id="yaml files",
        ),
    ]

    @pytest.mark.parametrize(
        ("allowed_extensions", "given_extensions", "expected_results"), extension_cases
    )
    def test_config_raises_exception_for_invalid_file_extensions(
        allowed_extensions: List[str],
        given_extensions: List[str],
        expected_exceptions: List[Optional[Exception]],
        mock_parser,
        tmp_path,
    ):
        for index, extension in enumerate(given_extensions):
            file = tmp_path / f"file.{extension}"
            expected_exception = expected_exceptions[index]

            with pytest.raises() if expected_exception is not None else nullcontext():
                config = Config(
                    allowed_extensions=allowed_extensions,
                    file=file,
                    parser=mock_parser(),
                )

            assert mock_parser.parse.assert_called_once()

    def test_config_returns_parsed_rules_as_property(mock_parser, tmp_path):
        expected_result = {"rule": "value"}
        file = tmp_path / "config.yaml"
        Parser = mock_parser()

        config = Config(allowed_extensions=("yaml", "yml"), file=file, parser=Parser)

        mock_parser.parse.assert_called_once()

        assert config.rules == expected_result

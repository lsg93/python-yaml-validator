# use generators/iterables for performance...
from importlib import metadata
from importlib.metadata import EntryPoint
from typing import Iterator
from unittest.mock import patch

import pytest
from stubs.test_filesystem_stubs import internal_filesystem_stub, invalid_filenames_stub


class TestRuleScanner:
    @pytest.fixture()
    def create_rule_fs(self, fs):
        def create_from_stub(stub: dict):
            # create fake file structure from stub
            for path, files in internal_filesystem_stub.items():
                for file in files:
                    fs.create_file(f"{path}/{file}")

        return create_from_stub

    def test_scanner_discovers_internal_rules_from_default_path(self, create_rule_fs):
        stub = internal_filesystem_stub
        create_rule_fs(stub)

        scanner = Scanner()
        rules = scanner.get_rules()

        expected_rules = [file for files in stub.values() for file in files]

        assert isinstance(rules, Iterator)
        assert len(expected_rules) == len(list(rules))

    def test_scanner_discovers_rules_from_external_packages(self, fs):
        # Create mock entry points
        mocked_entry_points = (
            EntryPoint(
                name="user_defined_rule",
                value="external-rules-package.rules:user_defined_rule",
                group="extra.rules",
            ),
            EntryPoint(
                name="another_user_defined_rule",
                value="external-rules-package.rules:another_user_defined_rule",
                group="extra.rules",
            ),
        )

        with patch.object(metadata, "entry_points", return_value=mocked_entry_points):
            scanner = Scanner()
            rules = scanner.get_rules()

            assert isinstance(rules, Iterator)
            assert len(mocked_entry_points) == len(list(rules))

    def test_scanner_ignores_rules_with_incorrect_filenames(self, create_rule_fs):
        stub = invalid_filenames_stub
        create_rule_fs(stub)

        scanner = Scanner()
        rules = scanner.get_rules()

        # Better to just hardcode expected output than duplicate logic from within the scanner here.
        expected_rules = ["first_rule.py", "second_rule.py", "third_rule.py"]

        assert isinstance(rules, Iterator)
        assert len(expected_rules) == len(list(rules))

    def test_scanner_returns_empty_iterator_if_no_rules_are_found(self, fs):
        scanner = Scanner()
        rules = scanner.get_rules()

        assert isinstance(rules, Iterator)
        assert list(rules) == []

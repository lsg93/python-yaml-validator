# use generators/iterables for performance...
import pytest
from stubs.test_filesystem_stubs import internal_filesystem_stub


class TestRuleScanner:
    @pytest.fixture()
    def create_rules_dir(self, fs):
        # create fake file structure from stub
        for path, files in internal_filesystem_stub.items():
            for file in files:
                fs.create_file(f"{path}/{file}")

        # yield the fixture so it can be used in the other tests.
        yield fs

    def test_scanner_finds_all_internal_rules_in_default_path(self):
        scanner = Scanner()
        rules = scanner.get_rules()

        expected_rules = [
            file for files in internal_filesystem_stub.values() for file in files
        ]

        assert isinstance(rules, list)
        assert len(expected_rules) == len(rules)

    def test_scanner_ignores_rules_with_incorrect_filenames(self): ...

    def test_scanner_finds_rules_from_external_packages(self): ...

    def test_scanner_throws_exception_if 

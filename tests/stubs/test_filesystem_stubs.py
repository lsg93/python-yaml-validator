internal_filesystem_stub = {
    "src/rules": ["first_rule.py"],
    "src/rules/folder": ["second_rule.py", "third_rule.py"],
}

invalid_filenames_stub = {
    "src/rules": ["__init__.py", "first_rule.py", "incorrectfilename.py"],
    "src/rules/folder": ["second_rule.py", "third_rule.py", "fourth_rule.txt"],
}

from src.models import Parser, Rules


class YAMLParser(Parser):
    def __init__(self):
        self.supported_formats = ("yaml", "yml")

    def parse() -> Rules:
        return Rules()

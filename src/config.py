from src.exceptions import InvalidConfigFileExtensionException
from src.models import ConfigData
from src.parser import Parser


class Config(object):
    def __init__(self, source: ConfigData, parser: Parser):
        self.source = source
        self.parser = parser
        self.rules = None

        try:
            self._validate_extension()
            self.rules = self.parser.parse(self.source)
        except Exception as e:
            raise e

    def _validate_extension(self):
        normalised_extension = self.source.format.removeprefix(".").lower()

        if normalised_extension not in [
            format.lower() for format in self.parser.supported_formats
        ]:
            raise InvalidConfigFileExtensionException

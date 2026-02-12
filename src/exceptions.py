# General exceptions
class InvalidArgumentException(Exception):
    pass


# CLI exceptions


class ConfigFileNotFoundException(Exception): ...


class InvalidConfigFileExtensionException(Exception): ...


# File loader exceptions
class LoaderFileNotFoundException(Exception): ...


# Parser exceptions


class ParserException(Exception): ...


class YAMLException(ParserException): ...


class EmptySourceException(ParserException): ...

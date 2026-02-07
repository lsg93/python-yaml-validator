# General exceptions
class InvalidArgumentException(Exception):
    pass


# CLI exceptions


class ConfigFileNotFoundException(Exception):
    pass


class InvalidConfigFileExtensionException(Exception):
    pass


# File loader exceptions
class LoaderFileNotFoundException(Exception):
    pass

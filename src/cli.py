from pathlib import Path


class NoDefaultConfigException(Exception):
    def __str__(self):
        return "Default config file not found in root folder."


class InvalidArgumentException(Exception):
    pass


ROOT_DIR = Path(__file__).parent.parent
DEFAULT_CONFIG_PATH = Path.joinpath(ROOT_DIR, "validator-config.yaml")


def get_default_config(path: Path = DEFAULT_CONFIG_PATH) -> Path:
    if path.exists() and path.is_file():
        return path
    raise NoDefaultConfigException()

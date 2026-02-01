from pathlib import Path
from typing import Optional

import pytest
from typer.testing import CliRunner

from main import app
from src.cli import DEFAULT_CONFIG_PATH


@pytest.fixture()
def cli():
    runner = CliRunner()

    def call_runner(args: list[str] = []):
        return runner.invoke(app, args, catch_exceptions=False)

    return call_runner


@pytest.fixture()
def config_path():
    # Can use cwd as pytest is running from root?
    default_path = Path.cwd().joinpath(DEFAULT_CONFIG_PATH)

    def create_config(path: Optional[Path] = default_path):
        if path == default_path:
            # Create default config file based on stub
            # I feel like you could use DI here to influence the path used by 'main()' but have no clue how to do that in Python...
            default_stub = Path(__file__).parent.joinpath(
                "stubs", "default_config_stub.yml"
            )
            default_stub.copy(default_path)

        if path.exists() is False or path.is_dir():
            raise Exception(f"No file found present at the given path {str(path)}")

        yield  # Test runs here.

        # Tear down created file
        if path.exists() and path == default_path:
            path.unlink()

    return create_config

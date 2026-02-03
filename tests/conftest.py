import json
from pathlib import Path
from typing import Optional

import pytest
from typer.testing import CliRunner

from main import app

default_config = {"hello": "world"}


@pytest.fixture()
def create_config(monkeypatch, tmp_path, config=default_config):
    default_path = tmp_path

    def create_config(path: Optional[Path] = default_path):
        if path == default_path:
            # monkeypatch env variable and write data to it.
            config_path = tmp_path / "config.file"
            monkeypatch.setenv("DEFAULT_CONFIG_PATH", str(config_path))
        else:
            config_path = tmp_path / path

        config_path.write_text(json.dumps(config))

    return create_config


@pytest.fixture()
def cli():
    runner = CliRunner()

    def call_runner(args: list[str] = []):
        return runner.invoke(app, args, catch_exceptions=False)

    return call_runner

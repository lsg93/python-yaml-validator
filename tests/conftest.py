import os

import pytest
from typer.testing import CliRunner

from main import app


@pytest.fixture()
def cli():
    runner = CliRunner()

    def call_runner(args: list[str]):
        return runner.invoke(app, args)

    return call_runner


@pytest.fixture()
def config_path():
    def create_config(yaml: str, path="../config.yaml"):
        target_output = os.path.join(path)
        with open(target_output, "w+"):
            target_output.write(yaml)
        return target_output

    return create_config

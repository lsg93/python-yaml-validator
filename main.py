from pathlib import Path
from typing import Annotated, Optional

import typer
from dotenv import load_dotenv

from src import Config, ConfigFileNotFoundException

# Load env vars for use in config.
load_dotenv()

app = typer.Typer()


def run(
    config_path: Annotated[
        Optional[Path],
        typer.Option(
            exists=True,
            file_okay=True,
            dir_okay=False,
            writable=False,
            readable=True,
            resolve_path=True,
        ),
    ] = None,
):
    try:
        config = Config()
        config.load_from_file(config_path)
    except (NoDefaultConfigException, ConfigFileNotFoundException) as e:
        typer.echo(f"Error : {str(e)}")
        typer.echo("Exiting with code 1")
        raise typer.Exit(code=1)
    except Exception:
        typer.echo("Error : Unknown error")
        typer.echo("Exiting with code 1")
        raise typer.Exit(code=1)

    # Next step is to pass things through a validator.
    # TODO

    raise typer.Exit(code=0)


@app.command()
def main(
    config_path: Annotated[
        Optional[Path],
        typer.Option(
            exists=True,
            file_okay=True,
            dir_okay=False,
            writable=False,
            readable=True,
            resolve_path=True,
        ),
    ] = None,
):
    run(config_path)


if __name__ == "__main__":
    app()

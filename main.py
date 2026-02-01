from pathlib import Path
from typing import Annotated, Optional

import typer

from src import NoDefaultConfigException, get_default_config

app = typer.Typer()


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
    config = ""
    if config_path is None:
        # Use default config or raise exception
        try:
            config = get_default_config()
        except NoDefaultConfigException as e:
            typer.echo(f"Error : {str(e)}")
            typer.echo("Exiting with code 1")
            raise typer.Exit(code=1)
        except Exception:
            typer.echo("Error : Unknown error")
            typer.echo("Exiting with code 1")
            raise typer.Exit(code=1)

    if config == "":
        # Typer takes care of checking if the path is valid.
        config = config_path.read_text()

    # Next step is to pass things through a validator.
    # TODO

    raise typer.Exit(code=0)


if __name__ == "__main__":
    app()

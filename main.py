import typer

app = typer.Typer()


@app.command()
def main():
    print("Hello from python-yaml-validator!")


if __name__ == "__main__":
    app()

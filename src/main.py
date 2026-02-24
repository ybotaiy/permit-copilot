import typer

app = typer.Typer(help="Permit Copilot – AI permit assistant.")


@app.command()
def hello(name: str = "world"):
    """Say hello (smoke-test that the CLI works)."""
    typer.echo(f"Hello, {name}!")


if __name__ == "__main__":
    app()

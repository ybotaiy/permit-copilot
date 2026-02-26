import typer

app = typer.Typer(help="Permit Copilot – AI permit assistant.")
ingest_app = typer.Typer(help="Ingest pipeline commands.")
app.add_typer(ingest_app, name="ingest")


@app.command()
def hello(name: str = "world"):
    """Say hello (smoke-test that the CLI works)."""
    typer.echo(f"Hello, {name}!")


@ingest_app.command("download")
def ingest_download(
    force: bool = typer.Option(False, help="Re-download existing files"),
):
    """Download KB documents from manifest."""
    from src.ingest.downloader import download_manifest

    download_manifest(force=force)


if __name__ == "__main__":
    app()

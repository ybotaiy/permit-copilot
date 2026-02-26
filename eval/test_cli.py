from typer.testing import CliRunner

from src.main import app

runner = CliRunner()


def test_app_imports():
    assert app is not None


def test_help_exits_cleanly():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "hello" in result.output.lower()
    assert "ingest" in result.output.lower()


def test_hello_default():
    result = runner.invoke(app, ["hello"])
    assert result.exit_code == 0
    assert "Hello, world!" in result.output

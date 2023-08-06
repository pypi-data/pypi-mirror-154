import pytest
from click.testing import CliRunner
from monkeytale import __version__, cli


def test_plain_cli():
    runner = CliRunner()
    result = runner.invoke(cli, [])
    assert result.exit_code == 0
    assert "monkeytale/monkeytale/__init__.py!" in result.output


def test_version_option():
    runner = CliRunner()
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert result.output == f"cli, version {__version__}\n"

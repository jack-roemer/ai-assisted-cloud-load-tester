from typer.testing import CliRunner

from load_tester.cli import app

runner = CliRunner()


def test_doctor_command() -> None:
    result = runner.invoke(app, ["doctor"])

    assert result.exit_code == 0
    assert "load-tester CLI is ready." in result.stdout

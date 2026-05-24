

from typer.testing import CliRunner

from src.configlog import main


runner = CliRunner()



def test_app():
    result = runner.invoke(main.app, ["init", "config.yaml"])
    assert result.exit_code == 0
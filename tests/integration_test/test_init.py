from typer.testing import CliRunner
import json

from cfglock import cli


runner = CliRunner()


def test_app():
    with runner.isolated_filesystem():
        with open("config.yaml", "w", encoding="utf-8") as f:
            f.write("name: demo\nenabled: true\n")

        result = runner.invoke(cli.app, ["init", "config.yaml"])
        assert result.exit_code == 0

        with open("config.lock.json", "r", encoding="utf-8") as f:
            lock_data = json.load(f)

        assert lock_data["version"] == 1

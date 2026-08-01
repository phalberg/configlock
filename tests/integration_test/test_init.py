import json

import yaml

from cfglock import cli


def test_init_correct(runner_setup, fixture_dir):
    fixture = fixture_dir / "config.yaml"

    with open(fixture, "r", encoding="utf-8") as f:
        output = yaml.safe_load(f)

    assert isinstance(output, dict)
    assert "environment" in output["app_settings"]

    result = runner_setup.invoke(cli.app, ["init", str(fixture)])

    with open("config.lock.json", "r") as f:
        output = json.load(f)

    assert result.exit_code == 0
    assert "environment" in output["app_settings"]
    assert output["version"] == 1
    # interesting case, false -> False (real boolean type)
    assert not output["app_settings"]["maintenance_mode"]

import json

import yaml

from cfglock import cli
from cfglock.validator import ConfigLockError


def test_sync_correct(runner_with_lock_file_setup, fixture_dir):
    fixture = fixture_dir / "config.yaml"

    with open(fixture, "r", encoding="utf-8") as f:
        output = yaml.safe_load(f)

    assert isinstance(output, dict)
    assert "environment" in output["app_settings"]

    result = runner_with_lock_file_setup.invoke(cli.app, ["sync", str(fixture)])

    with open("config.lock.json", "r") as f:
        output = json.load(f)

    assert result.exit_code == 0
    assert "environment" in output["app_settings"]
    assert output["version"] == 1
    # interesting case, false -> False (real boolean type)
    assert not output["app_settings"]["maintenance_mode"]


def test_sync_outdated_source_file(runner_with_lock_file_setup, fixture_dir):
    fixture = fixture_dir / "configbreak_namechange.yaml"

    with open(fixture, "r", encoding="utf-8") as f:
        yaml.safe_load(f)

    result = runner_with_lock_file_setup.invoke(cli.app, ["sync", str(fixture)])

    with open("config.lock.json", "r") as f:
        json.load(f)

    assert result.exit_code == 1
    assert isinstance(result.exception, ConfigLockError)
    assert "lock file is outdated" in str(result.exception).lower()


def test_sync_outdated_lock_file(runner_with_lock_file_setup, fixture_dir):
    fixture = fixture_dir / "config.yaml"

    with open("config.lock.json", "w", encoding="utf-8") as f:
        json.dump(
            {
                "app_settings": {
                    "environment": "production",  # changed from "staging"
                    "maintenance_mode": False,
                    "timeout_seconds": 30,
                },
                "version": 1,
            },
            f,
        )

    result = runner_with_lock_file_setup.invoke(cli.app, ["sync", str(fixture)])

    assert result.exit_code == 1
    assert isinstance(result.exception, ConfigLockError)
    assert "lock file is outdated" in str(result.exception).lower()

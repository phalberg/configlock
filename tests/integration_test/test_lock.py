import yaml
import json

from cfglock import cli
from cfglock.validator import ConfigLockError


def helper_ok(result, output):
    assert result.exit_code == 0
    assert output["version"] == 1
    # interesting case, false -> False (real boolean type)
    assert not output["app_settings"]["maintenance_mode"]


def helper_fail(result, error):
    assert result.exit_code == 1
    assert isinstance(result.exception, error)


def test_lock_correct(runner_setup, fixture_dir):
    fixture = fixture_dir / "config.yaml"

    with open(fixture, "r", encoding="utf-8") as f:
        output = yaml.safe_load(f)

    assert isinstance(output, dict)
    assert "environment" in output["app_settings"]

    result = runner_setup.invoke(cli.app, ["lock", str(fixture)])

    with open("config.lock.json", "r") as f:
        output = json.load(f)

    helper_ok(result, output)
    assert "environment" in output["app_settings"]


def test_lock_string_change_ok(runner_setup, fixture_dir):
    fixture = fixture_dir / "config_string_change.yaml"

    with open(fixture, "r", encoding="utf-8") as f:
        output = yaml.safe_load(f)

    assert isinstance(output, dict)
    assert "production" in output["app_settings"]["environment"]

    result = runner_setup.invoke(cli.app, ["lock", str(fixture)])

    with open("config.lock.json", "r") as f:
        output = json.load(f)

    helper_ok(result, output)
    assert "production" in output["app_settings"]["environment"]


def test_lock_add_on_change_ok(runner_setup, fixture_dir):
    fixture = fixture_dir / "config_add_on_change.yaml"

    with open(fixture, "r", encoding="utf-8") as f:
        output = yaml.safe_load(f)

    assert isinstance(output, dict)
    assert "ok" in output["app_settings"]["new_entry"]

    result = runner_setup.invoke(cli.app, ["lock", str(fixture)])

    with open("config.lock.json", "r") as f:
        output = json.load(f)

    helper_ok(result, output)
    assert "ok" in output["app_settings"]["new_entry"]


def test_lock_fail_namechange(runner_setup, fixture_dir):
    fixture = fixture_dir / "configbreak_namechange.yaml"

    with open(fixture, "r", encoding="utf-8") as f:
        output = yaml.safe_load(f)

    assert isinstance(output, dict)
    assert "staging" in output["app_settings"]["name_changed"]

    result = runner_setup.invoke(cli.app, ["lock", str(fixture)])

    print(result.exception)
    helper_fail(result, ConfigLockError)
    assert "lock" in str(result.exception).lower()
    print(result)

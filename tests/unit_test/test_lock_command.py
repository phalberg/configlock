import json

from cfglock import cli
from cfglock.validator import ConfigLockError, ValidationError


def test_lock_works(runner_with_lock_file_setup):

    with open("config.lock.json", "r") as f:
        output = json.load(f)

    # lock initialized from test fixture; check a known nested key/value
    assert "app_settings" in output
    assert output["app_settings"].get("environment") == "staging"

    # create a new config that matches the lock shape and add a new entry
    new_config = {
        "app_settings": {
            "environment": "staging",
            "maintenance_mode": False,
            "timeout_seconds": 30,
        },
        "new_entry": 10,
    }
    with open("config.json", "w", encoding="utf-8") as f:
        json.dump(new_config, f)

    result = runner_with_lock_file_setup.invoke(cli.app, ["lock", "config.json"])

    assert result.exit_code == 0

    with open("config.lock.json", "r") as f:
        output = json.load(f)

    assert output.get("new_entry") == 10


def test_no_lock_file_available(runner_with_file_setup):

    result = runner_with_file_setup.invoke(cli.app, ["lock", "config.json"])

    with open("config.json", "r") as f:
        output = json.load(f)

    # tests for config.lock.json
    assert "name" in output
    assert output["object"] is False

    assert result.exit_code == 1
    assert isinstance(result.exception, ConfigLockError)
    assert "lock file was not found" in str(result.exception).lower()


def test_not_available_file(runner_setup):

    result = runner_setup.invoke(cli.app, ["lock", "some_file.json"])

    assert result.exit_code == 1
    assert isinstance(result.exception, FileNotFoundError)


def test_compatibility_file(runner_with_lock_file_setup):

    with open("incompatible_file.toml", "w", encoding="utf-8") as f:
        f.write('[section]\nkey = "value"')

    result = runner_with_lock_file_setup.invoke(
        cli.app, ["lock", "incompatible_file.toml"]
    )

    assert result.exit_code == 1
    assert isinstance(result.exception, ValueError)
    assert "not able to read" in str(result.exception).lower()


def test_fail_new_key(runner_with_lock_file_setup):

    with open("new_file.yaml", "w", encoding="utf-8") as f:
        f.write("first_name: example")
    result = runner_with_lock_file_setup.invoke(cli.app, ["lock", "new_file.yaml"])

    assert result.exit_code == 1
    assert isinstance(result.exception, ValidationError)
    exc_str = str(result.exception).lower()
    assert all(s in exc_str for s in ["in path", "expected", "found", "error code"])


def test_fail_new_value(runner_with_lock_file_setup):
    # change type for a nested value (environment should be a string)
    with open("new_file.yaml", "w", encoding="utf-8") as f:
        f.write("app_settings:\n  environment: 12")
    result = runner_with_lock_file_setup.invoke(cli.app, ["lock", "new_file.yaml"])

    assert result.exit_code == 1
    assert isinstance(result.exception, ValidationError)
    exec_str = str(result.exception).lower()
    assert all(
        s in exec_str
        for s in [
            "in path",
            "<str>",
            "<int>",
            "12",
            "found",
            "expected",
            "error code",
        ]
    )


def test_order_matters_works(runner_with_lock_file_setup):

    with open("new_file.yaml", "w", encoding="utf-8") as f:
        f.write("object: false")

    result = runner_with_lock_file_setup.invoke(
        cli.app, ["lock", "new_file.yaml", "--order-matters"]
    )

    assert result.exit_code == 1
    assert isinstance(result.exception, ValidationError)
    exc_str = str(result.exception).lower()
    assert all(
        s in exc_str
        for s in ["in path", "expected", "found", "error code", "additional", "order"]
    )


def test_no_order_matters_works(runner_with_lock_file_setup):
    # create YAML with same content but different order
    with open("new_file.yaml", "w", encoding="utf-8") as f:
        f.write(
            "ai_prompts:\n  system_prompt: 'You are a helpful assistant.'\n  temperature: 0.7\n"
            "feature_flags:\n  enable_new_ui: true\n  beta_users_only: false\n"
            "app_settings:\n  timeout_seconds: 30\n  maintenance_mode: false\n  environment: 'staging'\n"
        )

    result = runner_with_lock_file_setup.invoke(cli.app, ["lock", "new_file.yaml"])

    assert result.exit_code == 0
    assert result.exception is None

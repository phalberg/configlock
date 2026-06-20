from cfglock import cli

from cfglock.validator import ValidationError
import json


def test_lock_works(runner_with_lock_file_setup):

    with open("config.lock.json", "r") as f:
        output = json.load(f)

    # tests for config.lock.json
    assert "name" in output
    assert output["object"] is False

    with open("config.json", "w", encoding="utf-8") as f:
        output = json.dump({"name": "example", "object": False, "new_entry": 10}, f)

    result = runner_with_lock_file_setup.invoke(cli.app, ["lock", "config.json"])

    assert result.exit_code == 0

    with open("config.lock.json", "r") as f:
        output = json.load(f)

    # tests for config.lock.json
    assert "name" in output
    assert output["object"] is False
    assert output["new_entry"] == 10


def test_no_lock_file_available():
    pass


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

    with open("new_file.yaml", "w", encoding="utf-8") as f:
        f.write("name: 12")
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
            "example",
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

    with open("new_file.yaml", "w", encoding="utf-8") as f:
        f.write("object: false\nname: example")

    result = runner_with_lock_file_setup.invoke(cli.app, ["lock", "new_file.yaml"])

    assert result.exit_code == 0
    assert result.exception is None

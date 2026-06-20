import json

from cfglock import cli


def test_init_works(runner_with_file_setup):

    result = runner_with_file_setup.invoke(cli.app, ["init", "config.json"])

    with open("config.json", "r") as f:
        output = json.load(f)

    # tests for config.json
    assert result.exit_code == 0
    assert "name" in output
    assert output["object"] is False

    with open("config.lock.json", "r") as f:
        output = json.load(f)

    # tests for config.lock.json (should match the input config.json)
    assert result.exit_code == 0
    assert "name" in output
    assert output["object"] is False


def test_init_valueerror_path_error(runner_setup):

    result = runner_setup.invoke(cli.app, ["init", "not_available_path"])

    assert result.exit_code == 1
    assert isinstance(result.exception, ValueError)
    assert "read the file" in str(result.exception).lower()


def test_init_path_already_exits(runner_with_lock_file_setup):

    result = runner_with_lock_file_setup.invoke(cli.app, ["init", "not_needed.json"])

    # confirming the files contents, as to not overwrite anything
    with open("config.lock.json", "r") as f:
        output = f.read()

    # the lock fixture is now derived from the YAML fixture; check a known key
    assert "app_settings" in str(output)
    assert "file already exists" in str(result.output).lower()


def test_not_supported_file(runner_setup):

    result = runner_setup.invoke(cli.app, ["init", "not_supported.toml"])

    assert result.exit_code == 1
    assert isinstance(result.exception, ValueError)
    assert "not able to read the file" in str(result.exception).lower()

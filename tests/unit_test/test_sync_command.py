from cfglock import cli
from cfglock.validator import ConfigLockError


def test_check_file_identicality(runner_with_lock_file_setup):
    # write YAML that matches the repository fixture `tests/test_files/config.yaml`
    with open("config.yaml", "w", encoding="utf-8") as f:
        f.write("version: 1\n\n")
        f.write(
            'app_settings:\n  environment: "staging"\n  maintenance_mode: false\n  timeout_seconds: 30\n'
        )

    result = runner_with_lock_file_setup.invoke(cli.app, ["sync", "config.yaml"])
    assert result.exit_code == 0
    assert result.exception is None


def test_outdated_lock_file(runner_with_lock_file_setup):

    with open("config.yaml", "w", encoding="utf-8") as f:
        f.write("name: example")
    result = runner_with_lock_file_setup.invoke(cli.app, ["sync", "config.yaml"])
    assert result.exit_code == 1
    assert isinstance(result.exception, ConfigLockError)
    assert "lock file is outdated" in str(result.exception).lower()

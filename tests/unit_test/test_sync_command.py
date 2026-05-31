from configlock import main
from configlock.exceptions import ConfigLockError




def test_check_file_identicality(runner_with_lock_file_setup):
    with open("config.yaml", "w", encoding="utf-8") as f:
        f.write("name: example\nobject: false")
    result = runner_with_lock_file_setup.invoke(main.app, ["sync", "config.yaml"])
    assert result.exit_code == 0
    assert isinstance(result.exception, type(None))


def test_outdated_lock_file(runner_with_lock_file_setup):
    
    with open("config.yaml", "w", encoding="utf-8") as f:
        f.write("name: example")
    result = runner_with_lock_file_setup.invoke(main.app, ["sync", "config.yaml"])
    assert result.exit_code == 1
    assert isinstance(result.exception, ConfigLockError)
    assert "lock file is outdated" in str(result.exception).lower()

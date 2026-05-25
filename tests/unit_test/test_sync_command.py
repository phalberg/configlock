from typer.testing import CliRunner
from configlog import main
import pytest
import json

runner = CliRunner()

def output_debbuging(result):
    print(result.output)
    print(result.exception)
    print(result.exc_info)

@pytest.fixture
def runner_setup():
    with runner.isolated_filesystem():
        yield runner
        
@pytest.fixture
def runner_with_lock_file_setup():
    with runner.isolated_filesystem():        
        with open("config.lock.json", "w", encoding="utf-8") as f:
            json.dump({"name": "example", "value": 42}, f)
        yield runner

def test_not_available_lock_file(runner_setup):
    
    result = runner_setup.invoke(main.app, ["sync", "some_file.json"])

    assert result.exit_code == 1
    assert isinstance(result.exception, FileNotFoundError)
    assert "no such file" in str(result.exception).lower()
    

def test_compatibility_file(runner_with_lock_file_setup):


    result = runner_with_lock_file_setup.invoke(main.app, ["sync", "incompatible_file.toml"])

    assert result.exit_code == 1
    assert isinstance(result.exception, ValueError)
    assert "not able to read" in str(result.exception).lower()


def test_fail_new_key(runner_with_lock_file_setup):
    
    
    with open("new_file.yaml", "w", encoding="utf-8") as f:
        f.write("name: demo\nenabled: true\n")
    result = runner_with_lock_file_setup.invoke(main.app, ["sync", "new_file.yaml"])
    
    output_debbuging(result)

def test_fail_new_value():
    pass


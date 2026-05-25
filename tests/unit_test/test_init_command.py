from typer.testing import CliRunner
from configlog import main
import pytest

runner = CliRunner()


@pytest.fixture
def runner_setup():
    with runner.isolated_filesystem():
        yield runner
        
@pytest.fixture
def runner_with_lock_file_setup():
    with runner.isolated_filesystem():        
        with open("config.lock.json", "w", encoding="utf-8") as f:
            f.write(".")
        yield runner


def test_init_valueerror_path_error(runner_setup):
         
    result = runner_setup.invoke(main.app, ["init", "not_available_path"])
        
    assert result.exit_code == 1
    assert isinstance(result.exception, ValueError)
    assert "read the file" in str(result.exception)
      
def test_init_path_already_exits(runner_with_lock_file_setup):
    
        
    result = runner_with_lock_file_setup.invoke(main.app, ["init", "not_needed.json"] )
        
    with open("config.lock.json", "r") as f:
        output = f.read()
            
    assert "." in str(output)
    assert "File already exists" in str(result.output)    
    
def test_not_supported_file(runner_setup):
    
    result = runner_setup.invoke(main.app, ["init", "not_supported.toml"])
    
    assert result.exit_code == 1
    assert isinstance(result.exception, ValueError)
    assert "not able to read the file" in str(result.exception)
    
    




    

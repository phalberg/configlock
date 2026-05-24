from typer.testing import CliRunner
from configlog import main
import pytest

runner = CliRunner()


@pytest.fixture
def setup():
    with runner.isolated_filesystem():
        yield runner

def test_init_valueerror_path_error(setup):
         
    result = setup.invoke(main.app, ["init", "not_available_path"])
        
    assert result.exit_code == 1
    assert isinstance(result.exception, ValueError)
    assert "read the file" in str(result.exception)
    
    print(result.output)
  
def test_init_path_already_exits(setup):
    
    with setup.isolated_filesystem():
        with open("config.lock.json", "w", encoding="utf-8") as f:
            f.write("name: demo\nenabled: true\n")

        result = runner.invoke(main.app, ["init", "duplicated.yaml"] )
        
    print(result.output)        
    



    

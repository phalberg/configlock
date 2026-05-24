from typer.testing import CliRunner
from configlog import main
import pytest

runner = CliRunner()



def test__init_command():

    with runner.isolated_filesystem():
        result = runner.invoke(main.app, ["init", "not_available_path"])
        
    assert result.exit_code == 1
    assert isinstance(result.exception, ValueError)
    assert "read the file" in str(result.exception)
  

    

from typer.testing import CliRunner
from configlog import main

runner = CliRunner()



def test_init_valueerror_path_error():

    with runner.isolated_filesystem():
        result = runner.invoke(main.app, ["init", "not_available_path"])
        
    assert result.exit_code == 1
    assert isinstance(result.exception, ValueError)
    assert "read the file" in str(result.exception)
  
  
def test_init_path_already_exits():
    
    pass



    

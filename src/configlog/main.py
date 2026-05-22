import typer

from helper import read_yaml, read_json, write_json, check_file_exists

from enum import Enum

class FileFormat(Enum):
    YAML = "yaml"
    JSON = "json"

app = typer.Typer()
SUPPORTED = {FileFormat.YAML, FileFormat.JSON}



active_formats = [f.name for f in FileFormat if f in SUPPORTED]
    

@app.command()
def init(file_path: str) -> None:
    """
    Reads a YAML config and generates a lockfile.
    """
    if check_file_exists():
        typer.echo("File already exists!")
    else:
        try:
            data= read_yaml(file_path)
        except FileNotFoundError:
            data = read_json(file_path)
        else:
            typer.echo(f"Was not able to read the file, make sure it is any of the following types: {active_formats}")
        
    write_json(data)


@app.command()
def sync(file_path: str):
    """
    Used to sync the lock file if compatible
    """

    # make sure init has been ran
    #init(file_path)
    # assume the old file already exists:



    # then 
    check_compatibility(file_path)




    
if __name__ == "__main__":
    app()





import typer
import json
#from datetime import datetime

from helper import read_yaml, write_json

app = typer.Typer()

@app.command()
def init(file_path: str):
    """
    Reads a YAML config and generates a lockfile.
    """
    # check if it has already been created or not here! 
    data=read_yaml(file_path)

    write_json(data)


@app.command()
def sync(file_path: str):

    # make sure init has been ran
    init(file_path)

    # then 




    
if __name__ == "__main__":
    app()





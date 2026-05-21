import typer
import json
#from datetime import datetime

from helper import traverse, read_yaml

app = typer.Typer()

@app.command()
def sync(file_path: str):
    """
    Reads a YAML config and generates a lockfile.
    """

    data=read_yaml(file_path)

    # write to a .json file
    with open('config.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)


    
if __name__ == "__main__":
    app()
import typer
import yaml
import json
#from datetime import datetime

from helper import traverse

app = typer.Typer()

@app.command()
def sync(file_path: str):
    """
    Reads a YAML config and generates a lockfile.
    """
    typer.echo(f"Reading {file_path}...")
    # Open file .yaml
    with open(file_path, "r") as f:
        data = yaml.safe_load(f)

    # write to a .json file
    with open('config.json', 'w') as json_file:
        # 'indent=4' makes the resulting JSON human-readable
        json.dump(data, json_file, indent=4)



    typer.echo(f"Successfully loaded {len(data)} top-level keys.")
    
if __name__ == "__main__":
    app()
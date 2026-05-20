import typer
import yaml
#import json
from datetime import datetime

app = typer.Typer()

@app.command()
def sync(file_path: str):
    """
    Reads a YAML config and generates a lockfile.
    """
    # 1. Read the YAML file
    typer.echo(f"Reading {file_path}...")
    with open(file_path, "r") as f:
        data = yaml.safe_load(f)
    
    # 2. Print it to prove it works
    typer.echo(f"Successfully loaded {len(data)} top-level keys.")
    
    # Next steps for you: Hash the data and save it as a lock.json file!

if __name__ == "__main__":
    app()
import typer
import yaml


def traverse(node):
    if isinstance(node, dict):
        for key, value in node.items():
            print(f"Entering Key: {key}")
            traverse(value)
    elif isinstance(node, list):
        for item in node:
            traverse(item)
    else:
        # This is a leaf node (string, int, etc.)
        print(f"Value: {node}")



def read_yaml(file_path: str):
    typer.echo(f"Reading {file_path}...")
    try:
        with open(file_path, "r") as f:
            data = yaml.safe_load(f)
    except FileNotFoundError:
        raise
    else:
        typer.echo(f"Sucessfully read file")
    return data

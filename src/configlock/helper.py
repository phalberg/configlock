import typer
import yaml
import json
from pathlib import Path
import filecmp
from dotenv import load_dotenv
import os

load_dotenv()
CONFIG_LOG_FILE_PATH = os.getenv('CONFIG_LOG_FILE_PATH', 'config.lock.json')



def check_file_identicality(file_path:str, config_file_path: str | None = CONFIG_LOG_FILE_PATH):
    
    filecmp.clear_cache()
    are_files_identical = filecmp.cmp(file_path, config_file_path, shallow=False)
    return are_files_identical
    
    

def check_file_exists(file_path: str | None = CONFIG_LOG_FILE_PATH) -> bool:
    path = Path(file_path)
    exists = path.exists()
    if not exists:
        typer.echo(f"The path does not exist: {path}")
    return exists



def read_yaml(file_path: str) -> dict:
    try:
        with open(file_path, "r") as f:
            data = yaml.safe_load(f)
    except FileNotFoundError:
        raise
    else:
        typer.echo(f"Sucessfully read file")
    return data


def read_json(file_path: str) -> dict:
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        raise
    else:
        typer.echo(f"Sucessfully read file")
    return data
    
def write_json(data: dict, file_path: str | None = CONFIG_LOG_FILE_PATH) -> None:
    data.update({"version": 1})
    try:
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
    except TypeError:
        raise
    except Exception:
        raise
    else:
        typer.echo(f"Sucessfully wrote file")


def check_file_and_read_file(file_path: str) -> dict:
    typer.echo(f"Reading {file_path}...")

    path = Path(file_path)
    suffix = path.suffix.lower()

    reader_by_suffix = {
        ".yaml": read_yaml,
        ".yml": read_yaml,
        ".json": read_json,
    }

    reader = reader_by_suffix.get(suffix)
    if reader is None:
        typer.echo(
            f"File not suppported: {suffix}. Use .yaml, .yml, or .json.",
            err=True,
        )
        raise ValueError("Error not able to read the file")

    data = reader(file_path)

    return data

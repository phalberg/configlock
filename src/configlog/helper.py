import typer
import yaml
import json
from pathlib import Path

CONFIG_LOG_FILE_PATH = "config.lock.json"



def check_file_exists(file_path: str | None = CONFIG_LOG_FILE_PATH) -> bool:
    path = Path(file_path)
    exists = Path.is_file(path)
    return exists



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


def check_compatibility():

    """"
    Keys => same names (must be the same, and (!) in the same (?order?)/precedence)
Values => must be of the same types
What about adding New entries? -> Fine
Deleting entries should not be allowed as it will obviously destroy Things. -> Fail
    """


    pass

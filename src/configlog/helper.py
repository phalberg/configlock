import typer
import yaml
import json
from enum import Enum
from pathlib import Path

from itertools import zip_longest


CONFIG_LOG_FILE_PATH = "config.lock.json"

class SupportedFiles(Enum):
    YAML = ["yaml", "yml"]
    JSON = ["json"]
    TOML = []

active_formats = [f for f in SupportedFiles if f.value]
keys_to_ignore = {"version"}



def check_file_exists(file_path: str | None = CONFIG_LOG_FILE_PATH) -> bool:
    path = Path(file_path)
    exists = Path.is_file(path)
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


    if suffix in [".yaml", ".yml"]:
        data = read_yaml(file_path)
    elif(suffix == ".json"):
        data = read_json(file_path)
    else:
        typer.echo(f"File not suppported: {suffix}", err=True)
        typer.echo(f"Was not able to read the file, make sure it is any of the following types: {active_formats}", err=True)
        raise ValueError("Error not able to read the file")

    return data



def check_compatibility(new_file_path: str) -> None:
    """"
    Keys => same names (must be the same, and (!) in the same (?order?)/precedence)
    Values => must be of the same types
    What about adding New entries? -> Fine
    Deleting entries should not be allowed as it will obviously destroy Things. -> Fail
    """

    # implement some DFS algorithm to run this.

    current_file_path = CONFIG_LOG_FILE_PATH

    

    current_data = read_json(current_file_path)
    new_data = check_file_and_read_file(new_file_path)


    walk_yaml(current_data, new_data)



def walk_yaml(current_data, new_data, depth=0):
    """Recursively walks through a YAML-loaded object."""
    # Indentation for visual clarity during printing
    indent = "  " * depth

    if isinstance(current_data, dict):
        for new_pair, curr_pair in zip_longest(new_data.items(), current_data.items(), fillvalue=(None, None)):
            new_k, new_v = new_pair
            curr_k, curr_v = curr_pair


             # specific values for our own interpretation of versionings etc.
            if curr_k in keys_to_ignore:
                continue
        
            accept_new_keys(curr_k, new_k)


            print(f"{indent}New key: {new_k}, old key: {curr_k}, {type(curr_k)}")
            walk_yaml(new_v, curr_v , depth + 1)
            
 #   elif isinstance(current_data, list):
 #       for index, item in enumerate(current_data):
 #           print(f"{indent}Index {index}:")
 #           walk_yaml(item, depth + 1)
            
    else:
        accept_new_value(current_value=current_data, new_value=new_data)
        print(f"{indent}Value_old: {current_data}, and new_value: {new_data} its type_old {type(current_data)})")



def accept_new_keys(current_key: str, new_key: str) -> None:
    """
    General logic for accepting new keys:
    1) the name of new_key cannot be different than the name of current_key
    2) the order of new_key cannot be different than the current_key
    3) the precedence (i.e indentation) cannot be different than the current_key
    """

    if current_key != new_key:
            typer.echo(f"A key is missing or changed from {current_key} to {new_key}", err=True)
            raise ValueError(f"New proposed file does not match keys of lock file in {CONFIG_LOG_FILE_PATH}")
    


def accept_new_value(current_value, new_value) -> None:
    """
    General logic for accepting new values:
    1) the type of the new_value cannot be different than the type of the current_value
    """

    if type(current_value) != type(new_value):
            typer.echo(f"The type of a value has changed from {type(current_value)} to {type(new_value)}", err=True)
            raise ValueError(f"New proposed file does not match value type of lock file in {CONFIG_LOG_FILE_PATH}")


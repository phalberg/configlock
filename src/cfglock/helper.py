import typer
import yaml
import json
from pathlib import Path
import filecmp
from dotenv import load_dotenv
import os

from cfglock.validator import (
    ValidationContext,
    walk_yaml_in_order,
    walk_yaml_with_no_order,
)

load_dotenv()
CONFIG_LOG_FILE_PATH: str = os.environ.get("CONFIG_LOG_FILE_PATH", "config.lock.json")


def check_file_identicality(
    file_path: str, config_file_path: str = CONFIG_LOG_FILE_PATH
):
    """Checks if files are identical, if they are it returns True, False otherwise"""
    try:
        a = check_file_and_read_file(file_path)
        b = read_json(config_file_path)
        if a == b:
            return True
        filecmp.clear_cache()
        res = filecmp.cmp(file_path, config_file_path, shallow=False)
        return res
    except Exception:
        filecmp.clear_cache()
        res = filecmp.cmp(file_path, config_file_path, shallow=False)
        return res


def check_file_exists(file_path: str = CONFIG_LOG_FILE_PATH) -> bool:
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
        typer.echo("Sucessfully read file")
    return data


def read_json(file_path: str) -> dict:
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        raise
    else:
        typer.echo("Sucessfully read file")
    return data


def write_json(data: dict, file_path: str = CONFIG_LOG_FILE_PATH) -> None:
    data.update({"version": 1})
    try:
        with open(file_path, "w") as json_file:
            json.dump(data, json_file, indent=4)
    except TypeError:
        raise
    except Exception:
        raise
    else:
        typer.echo("Sucessfully wrote file")


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


def check_comp_cli(new_file_path: str, order_matters: bool = False) -> None:
    """ ""
    Check compatiblity for the cli version
    Keys => same names (must be the same, and (!) in the same (?order?)/precedence)
    Values => must be of the same types
    What about adding New entries? -> Fine
    Deleting entries should not be allowed as it will obviously destroy Things. -> Fail
    """

    current_file_path = CONFIG_LOG_FILE_PATH
    context = ValidationContext(
        new_path=new_file_path,
        current_path=current_file_path,
        order_matters=bool(order_matters),
    )

    current_data = read_json(current_file_path)
    new_data = check_file_and_read_file(new_file_path)

    if order_matters:
        walk_yaml_in_order(current_data, new_data, context)
    else:
        walk_yaml_with_no_order(current_data, new_data, context)

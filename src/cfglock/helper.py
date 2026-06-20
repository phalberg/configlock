import typer
import yaml
import json
from pathlib import Path
import filecmp
from dotenv import load_dotenv
import os

from cfglock.validator import (
    ConfigLockError,
    ValidationContext,
    walk_yaml_in_order,
    walk_yaml_with_no_order,
    keys_to_ignore,
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

        # metadata we do not care about
        if isinstance(a, dict):
            a = {k: v for k, v in a.items() if k not in keys_to_ignore}
        if isinstance(b, dict):
            b = {k: v for k, v in b.items() if k not in keys_to_ignore}

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
    except TypeError as exc:
        raise TypeError(f"Data could not be serialized to JSON: {exc}") from exc
    except OSError as exc:
        raise OSError(f"Could not write JSON file at {file_path}: {exc}") from exc
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


def check_compatibility(new_file_path: str, order_matters: bool = False) -> None:
    """ ""
    Check compatiblity for two files given the file paths
    1) Keys must be same as previous keys, and order_matters can determine if the order also matters
    2) Values must have the same types as previously
    3) Adding new entries is allowed
    4) Deleting entries is not allowed
    """
    # the lock file
    current_file_path = CONFIG_LOG_FILE_PATH
    context = ValidationContext(
        new_path=new_file_path,
        current_path=current_file_path,
        order_matters=order_matters,
    )

    new_data = check_file_and_read_file(new_file_path)

    try:
        current_data = read_json(current_file_path)
    except FileNotFoundError:
        raise ConfigLockError("lock file was not found, please use init")

    if order_matters:
        walk_yaml_in_order(current_data, new_data, context)
    else:
        walk_yaml_with_no_order(current_data, new_data, context)

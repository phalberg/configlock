import filecmp
import json
import os
from abc import ABC, abstractmethod
from pathlib import Path

import typer
import yaml
from dotenv import load_dotenv

from cfglock.validator import (
    ConfigLockError,
    ValidationContext,
    keys_to_ignore,
    walk_yaml_in_order,
    walk_yaml_with_no_order,
)

load_dotenv()
CONFIG_LOG_FILE_PATH: str = os.environ.get("CONFIG_LOG_FILE_PATH", "config.lock.json")

# TODO: remove typer.echo at some point!


class FileReader(ABC):
    @abstractmethod
    def read(self, file_path: str) -> dict:
        """Reads the appropriate file."""


class YamlReader(FileReader):
    def read(self, file_path: str) -> dict:
        with open(file_path, "r") as f:
            data = yaml.safe_load(f) or {}

            if not isinstance(data, dict):
                raise TypeError(
                    f"Expected YAML object/dict in {file_path}, got {type(data).__name__}"
                )
        typer.echo("Successfully read file")
        return data


class JsonReader(FileReader):
    def read(self, file_path: str) -> dict:
        with open(file_path, "r") as f:
            data = json.load(f) or {}

            if not isinstance(data, dict):
                raise TypeError(
                    f"Expected JSON in {file_path}, got {type(data).__name__}"
                )

        typer.echo("Successfully read file")
        return data


class FileReaderFactory:
    reader = {
        ".yaml": YamlReader(),
        ".yml": YamlReader(),
        ".json": JsonReader(),
    }

    @classmethod
    def load(cls, file_path: str) -> dict:
        """Loads the relevant filetype.
        args
            file_path(str): str representation of file path.
        returns
            a dictionary with the contents of the file
        """
        # TODO: fix the file_path being only str, it can be Path also!

        path = Path(file_path)
        suffix = path.suffix.lower()

        reader = cls.reader.get(suffix)

        if not reader:
            typer.echo(
                f"File not suppported: {suffix}. Use .yaml, .yml, or .json.",
                err=True,
            )
            raise ValueError("Error not able to read the file")

        typer.echo(f"Reading {file_path}...")
        return reader.read(file_path)


def check_file_identicality(
    file_path: str, config_file_path: str = CONFIG_LOG_FILE_PATH
):
    """Checks if files are identical, if they are it returns True, False otherwise"""
    try:
        a = FileReaderFactory.load(file_path)
        b = FileReaderFactory.load(config_file_path)

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
        typer.echo("Successfully wrote file")


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
    new_data = FileReaderFactory.load(new_file_path)

    try:
        current_data = FileReaderFactory.load(current_file_path)
    except FileNotFoundError:
        raise ConfigLockError("lock file was not found, please use init")

    if order_matters:
        walk_yaml_in_order(current_data, new_data, context)
    else:
        walk_yaml_with_no_order(current_data, new_data, context)

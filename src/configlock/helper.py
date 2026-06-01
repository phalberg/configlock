import typer
import yaml
import json
from pathlib import Path
import filecmp
from dotenv import load_dotenv
import os

from configlock.exceptions import ConfigLockError

load_dotenv()
CONFIG_LOG_FILE_PATH = os.getenv('CONFIG_LOG_FILE_PATH', 'config.lock.json')



def check_file_identicality(file_path:str, config_file_path: str | None = CONFIG_LOG_FILE_PATH):
    """Checks if files are identical, if they are it returns True, False otherwise"""
    try:
        a = check_file_and_read_file(file_path)
        b = read_json(config_file_path)
        if a == b:
            return True
        filecmp.clear_cache()
        res = filecmp.cmp(file_path, config_file_path, shallow=False)
        return res
    except Exception as exc:
        filecmp.clear_cache()
        res = filecmp.cmp(file_path, config_file_path, shallow=False)
        return res
    
    

def check_file_exists(file_path: str | None = CONFIG_LOG_FILE_PATH) -> bool:
    path = Path(file_path)
    exists = path.exists()
    if not exists:
        typer.echo(f"The path does not exist: {path}")
    return exists


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


def check_file_and_read_file(file: dict) -> dict:

    data = detect_and_load(file)

    return data




def detect_and_load(data):
    
    try:
        data = json.loads(data)
        return data
    except ValueError:
        pass  # Content is not valid JSON        
    try:
        data = yaml.safe_load(data)
        return data
    except yaml.YAMLError:
        raise ConfigLockError("File is not of a supported file", error_code=1)


from itertools import zip_longest

import typer


from configlog.helper import check_file_and_read_file, read_json
from dotenv import load_dotenv
import os

load_dotenv()
CONFIG_LOG_FILE_PATH = os.getenv('CONFIG_LOG_FILE_PATH', 'config.lock.json')

keys_to_ignore = {"version"}



def check_compatibility(new_file_path: str, order_matters: bool | None = False) -> None:
    """"
    
    Keys => same names (must be the same, and (!) in the same (?order?)/precedence)
    Values => must be of the same types
    What about adding New entries? -> Fine
    Deleting entries should not be allowed as it will obviously destroy Things. -> Fail
    """

    current_file_path = CONFIG_LOG_FILE_PATH    

    current_data = read_json(current_file_path)
    new_data = check_file_and_read_file(new_file_path)

    if order_matters:
        walk_yaml_in_order(current_data, new_data)
    else:
        walk_yaml_with_no_order(current_data, new_data)



def walk_yaml_with_no_order(current_data, new_data, depth=0):
    """Recursively walks through a YAML-loaded object with no order."""
    # Indentation for visual clarity during printing
    indent = "  " * depth

    if isinstance(current_data, dict):
        if not isinstance(new_data, dict):
            accept_new_value(current_value=current_data, new_value=new_data)
            return

        for curr_k, curr_v in current_data.items():
            # specific values for our own interpretation of versionings etc.
            if curr_k in keys_to_ignore:
                continue

            if curr_k not in new_data:
                accept_new_keys(curr_k, None)

            new_v = new_data[curr_k]

            print(f"{indent}New key: {curr_k}, old key: {curr_k}, {type(curr_k)}")
            walk_yaml_with_no_order(curr_v, new_v, depth + 1)
            
 #   elif isinstance(current_data, list):
 #       for index, item in enumerate(current_data):
 #           print(f"{indent}Index {index}:")
 #           walk_yaml(item, depth + 1)
            
    else:
        accept_new_value(current_value=current_data, new_value=new_data)
        print(f"{indent}Value_old: {current_data}, and new_value: {new_data} its type_old {type(current_data)})")


def walk_yaml_in_order(current_data, new_data, depth=0):
    """Recursively walks through a YAML-loaded object in order."""
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
            walk_yaml_with_no_order(new_v, curr_v , depth + 1)
            
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
            typer.echo(f"The type of a value has changed from {type(current_value).__name__} to {type(new_value).__name__}", err=True)
            raise ValueError(f"New proposed file does not match value type of lock file in {CONFIG_LOG_FILE_PATH}")


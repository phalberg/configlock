from dataclasses import dataclass
from itertools import zip_longest

import typer


from .helper import check_file_and_read_file, read_json
from dotenv import load_dotenv
import os

from .exceptions import ValidationError  

load_dotenv()
CONFIG_LOG_FILE_PATH = os.getenv('CONFIG_LOG_FILE_PATH', 'config.lock.json')

keys_to_ignore = {"version"}



@dataclass
class ValidationContext:
    new_path: str
    current_path: str
    order_matters: bool

# add other metadata if needed.


def check_compatibility(new_file_path: str, order_matters: bool | None = False) -> None:
    """""
    
    Keys => same names (must be the same, and (!) in the same (?order?)/precedence)
    Values => must be of the same types
    What about adding New entries? -> Fine
    Deleting entries should not be allowed as it will obviously destroy Things. -> Fail
    """

    current_file_path = CONFIG_LOG_FILE_PATH
    context = ValidationContext(
        new_path=new_file_path,
        current_path=current_file_path,
        order_matters=bool(order_matters)
    )

    current_data = read_json(current_file_path)
    new_data = check_file_and_read_file(new_file_path)

    if order_matters:
        walk_yaml_in_order(current_data, new_data, context)
    else:
        walk_yaml_with_no_order(current_data, new_data, context)



def walk_yaml_with_no_order(current_data, new_data, context: ValidationContext, depth=0):
    """Recursively walks through a YAML-loaded object with no order."""

    if isinstance(current_data, dict):
        if not isinstance(new_data, dict):
            accept_new_value(current_value=current_data, new_value=new_data, context=context)
            return

        for curr_k, curr_v in current_data.items():
            # specific values for our own interpretation of versionings etc.
            if curr_k in keys_to_ignore:
                continue

            if curr_k not in new_data:
                accept_new_keys(curr_k, None, context)

            new_v = new_data[curr_k]

            walk_yaml_with_no_order(curr_v, new_v, context, depth + 1)
            
    else:
        accept_new_value(current_value=current_data, new_value=new_data, context=context)


def walk_yaml_in_order(current_data, new_data, context: ValidationContext, depth=0):
    """Recursively walks through a YAML-loaded object in order."""

    if isinstance(current_data, dict):
        for new_pair, curr_pair in zip_longest(new_data.items(), current_data.items(), fillvalue=(None, None)):
            new_k, new_v = new_pair
            curr_k, curr_v = curr_pair

            # specific values for our own interpretation of versionings etc.
            if curr_k in keys_to_ignore:
                continue
        
            accept_new_keys(current_key=curr_k, new_key=new_k, context=context)

            walk_yaml_with_no_order(new_v, curr_v, context, depth + 1)
            
    else:
        accept_new_value(current_value=current_data, new_value=new_data, context=context)




def accept_new_keys(current_key: str, new_key: str, context: ValidationContext) -> None:
    """
    General logic for accepting new keys:
    1) the name of new_key cannot be different than the name of current_key
    2) the order of new_key cannot be different than the current_key
    3) the precedence (i.e indentation) cannot be different than the current_key
    """

    if current_key != new_key:
            if context.order_matters:
                raise ValidationError(
                    path= context.new_path,
                    expected_value=current_key, 
                    actual_value=new_key,
                    order_matters=True
                )
            else:
                raise ValidationError(
                    path=context.new_path,
                    expected_value=current_key, 
                    actual_value=new_key,
                    order_matters=False
                )
    


def accept_new_value(current_value, new_value, context: ValidationContext) -> None:
    """
    General logic for accepting new values:
    1) the type of the new_value cannot be different than the type of the current_value
    """
    type_curr = type(current_value)
    type_new = type(new_value)
    
    if type_curr != type_new:
        
            type_curr_val = f"<{type_curr.__name__}> with value: {current_value}"
            type_next_val = f"<{type_new.__name__}> with value: {new_value}"

            raise ValidationError(
                path = context.new_path,
                expected_value=type_curr_val,
                actual_value=type_next_val
            )
        

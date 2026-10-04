from _typeshed import Incomplete
from dataclasses import dataclass

keys_to_ignore: Incomplete

@dataclass
class ValidationContext:
    new_path: str
    current_path: str
    order_matters: bool

class ConfigLockError(Exception):
    message: Incomplete
    error_code: Incomplete
    def __init__(self, message, error_code: int = 1) -> None: ...

class ValidationError(ConfigLockError):
    path: Incomplete
    expected_value: Incomplete
    actual_value: Incomplete
    order_matters: Incomplete
    def __init__(
        self,
        path,
        expected_value,
        actual_value,
        message: str = "Validation Failed",
        order_matters: bool = False,
    ) -> None: ...

def walk_yaml_with_no_order(
    current_data, new_data, context: ValidationContext, depth: int = 0
): ...
def walk_yaml_in_order(
    current_data, new_data, context: ValidationContext, depth: int = 0
): ...
def accept_new_keys(
    current_key: str | None, new_key: str | None, context: ValidationContext
) -> None: ...
def accept_new_value(current_value, new_value, context: ValidationContext) -> None: ...

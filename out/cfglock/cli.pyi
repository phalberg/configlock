from .helper import (
    FileReaderFactory as FileReaderFactory,
    check_compatibility as check_compatibility,
    check_file_exists as check_file_exists,
    check_file_identicality as check_file_identicality,
    write_json as write_json,
)
from _typeshed import Incomplete
from cfglock.validator import ConfigLockError as ConfigLockError
from typing import Annotated

app: Incomplete

def init(file_path: Annotated[str, None]) -> None: ...
def sync(file_path: Annotated[str, None]) -> None: ...
def lock(file_path: Annotated[str, None], order_matters: bool = ...) -> None: ...

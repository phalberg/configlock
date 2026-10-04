import abc
from abc import ABC, abstractmethod
from cfglock.validator import (
    ConfigLockError as ConfigLockError,
    ValidationContext as ValidationContext,
    keys_to_ignore as keys_to_ignore,
    walk_yaml_in_order as walk_yaml_in_order,
    walk_yaml_with_no_order as walk_yaml_with_no_order,
)
from collections.abc import Mapping as Mapping
from typing import Any, ClassVar

CONFIG_LOG_FILE_PATH: str
type MappingValue = dict[str, Any]

class FileReader[T: Mapping[str, Any]](ABC, metaclass=abc.ABCMeta):
    @abstractmethod
    def read(self, file_path: str) -> T: ...

class YamlReader(FileReader[MappingValue]):
    def read(self, file_path: str) -> MappingValue: ...

class JsonReader(FileReader[MappingValue]):
    def read(self, file_path: str) -> MappingValue: ...

class FileReaderFactory:
    reader: ClassVar[dict[str, FileReader[MappingValue]]]
    @classmethod
    def load(cls, file_path: str) -> MappingValue: ...

def check_file_identicality(file_path: str, config_file_path: str = ...) -> bool: ...
def check_file_exists(file_path: str | None = None) -> bool: ...
def write_json(data: MappingValue, file_path: str | None = None) -> None: ...
def check_compatibility(
    new_file_path: str,
    curr_file_path: str | None = None,
    *,
    order_matters: bool = False,
) -> None: ...

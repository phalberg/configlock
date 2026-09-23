from typing import Annotated
from pathlib import Path

import typer

from cfglock.validator import ConfigLockError

from .helper import (
    FileReaderFactory,
    check_compatibility,
    check_file_exists,
    check_file_identicality,
    write_json,
)

app = typer.Typer(help="ConfigLock: Secure GitOps YAML validation engine.")


@app.command()
def init(
    file_path: Annotated[
        str, typer.Argument(help="the path for the newly proposed file")
    ],
) -> None:
    """
    Reads a YAML config and generates a lockfile.
    """
    if check_file_exists(file_path):
        typer.echo("File already exists!")
    else:
        data = FileReaderFactory.load(file_path)
        parent = Path(file_path).parent
        write_json(data, parent)


@app.command()
def sync(
    file_path: Annotated[
        str, typer.Argument(help="the path for the newly proposed file")
    ],
) -> None:
    """
    Used to check if lock file and proposed file are out of sync
    """
    if check_file_identicality(file_path):
        typer.echo("The file has not changed.")
    else:
        raise ConfigLockError(
            "The lock file is outdated, run lock to update the lock file!", error_code=1
        )


@app.command()
def lock(
    file_path: Annotated[
        str, typer.Argument(help="the path for the newly proposed file")
    ],
    order_matters: bool = typer.Option(
        False,
        "--order-matters/--no-order-matters",
        help="choose if the order of the keys matter or not",
    ),
) -> None:
    """
    Used to update the lock file, IF compatible
    """
    if check_file_exists(file_path):
        check_compatibility(file_path, order_matters=order_matters)
        data = FileReaderFactory.load(file_path)
        parent = Path(file_path).parent
        write_json(data, parent)
    else:
        typer.echo("File does not exist, please create a lock file using init first.")
        raise ConfigLockError("lock file was not found, please create it first")

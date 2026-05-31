import typer

from configlock.exceptions import ConfigLockError

from .helper import  write_json, check_file_exists, check_file_identicality
from .validator import check_compatibility, check_file_and_read_file
from typing import Annotated

app = typer.Typer()


def main() -> None:
    app()


@app.command()
def init(file_path: Annotated[str, typer.Argument(help="the path for the newly proposed file")]) -> None:
    """
    Reads a YAML config and generates a lockfile.
    """
    if check_file_exists():
        typer.echo("File already exists!")
    else:
        data = check_file_and_read_file(file_path)
        write_json(data)


@app.command()
def sync(
    file_path: Annotated[str, typer.Argument(help="the path for the newly proposed file")],
) -> None:
    """
    Used to check if lock file and proposed file are out of sync
    """
    if check_file_identicality(file_path):
        typer.echo("The file has not changed.", err=True)
    else:
        raise ConfigLockError("The lock file is outdated, run sync to update the lock file!", error_code=1)


@app.command()
def lock(
    file_path: Annotated[str, typer.Argument(help="the path for the newly proposed file")],
    order_matters: bool = typer.Option(False, "--order-matters/--no-order-matters", help="choose if the order of the keys matter or not"),
    ) -> None:
    """
    Used to update the lock file, IF compatible
    """
    
    check_compatibility(file_path, order_matters)
    data = check_file_and_read_file(file_path)
    write_json(data)


    
if __name__ == "__main__":
    main()



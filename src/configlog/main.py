import typer

from .helper import  write_json, check_file_exists, check_compatibility, check_file_and_read_file, check_file_identicality
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
    order_matters: bool = typer.Option(False, "--order-matters/--no-order-matters", help="choose if the order of the keys matter or not"),
):
    """
    Used to sync the lock file if compatible
    """
    
    if check_file_identicality(file_path):
        typer.echo("The file has not changed.", err=True)
    else:  
        check_compatibility(file_path, order_matters)
        data = check_file_and_read_file(file_path)
        write_json(data)


    
if __name__ == "__main__":
    main()





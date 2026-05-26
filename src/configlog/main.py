import typer

from .helper import  write_json, check_file_exists, check_compatibility, check_file_and_read_file, check_file_identicality


app = typer.Typer()


def main() -> None:
    app()


@app.command()
def init(file_path: str) -> None:
    """
    Reads a YAML config and generates a lockfile.
    """
    if check_file_exists():
        typer.echo("File already exists!")
    else:
        data = check_file_and_read_file(file_path)
        write_json(data)


@app.command()
def sync(file_path: str):
    """
    Used to sync the lock file if compatible
    """
    
    if check_file_identicality(file_path):
        typer.echo("The file has not changed.", err=True)
    else:  
        check_compatibility(file_path)
        data = check_file_and_read_file(file_path)
        write_json(data)




    
if __name__ == "__main__":
    main()





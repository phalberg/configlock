import typer

from helper import  write_json, check_file_exists, check_compatibility, check_file_and_read_file


app = typer.Typer()


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

    # make sure init has been ran
    #init(file_path)
    # assume the old file already exists:

    check_compatibility(file_path)
    data = check_file_and_read_file(file_path)
    write_json(data)




    
if __name__ == "__main__":
    app()





import typer

from helper import read_yaml, write_json, check_file_exists

app = typer.Typer()

@app.command()
def init(file_path: str) -> None:
    """
    Reads a YAML config and generates a lockfile.
    """
    if check_file_exists():
        typer.echo("File already exists!")
    else:
        data=read_yaml(file_path)
        write_json(data)


@app.command()
def sync(file_path: str):
    """
    Used to sync the lock file if compatible
    """

    # make sure init has been ran
    init(file_path)

    # then 
    check_compatibility()




    
if __name__ == "__main__":
    app()





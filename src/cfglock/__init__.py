from pathlib import Path

from dotenv import load_dotenv

from . import cli

env_file = Path(".env")
if env_file.exists():
    load_dotenv(env_file)
else:
    load_dotenv(Path(".env.example"))


__all__ = cli

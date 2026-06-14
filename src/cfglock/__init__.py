from pathlib import Path
from dotenv import load_dotenv

env_file = Path(".env")
if env_file.exists():
    load_dotenv(env_file)
else:
    load_dotenv(Path(".env.example"))

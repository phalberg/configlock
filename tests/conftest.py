import json
import yaml
from pathlib import Path

from typing import Generator
import pytest
from typer.testing import CliRunner


@pytest.fixture
def fixture_dir() -> Generator[Path, None, None]:
    yield Path(__file__).resolve().parent / "test_files"


@pytest.fixture(name="runner")
def runner_setup() -> Generator[CliRunner, None, None]:
    runner = CliRunner()
    yield runner


@pytest.fixture
def runner_with_lockfile(
    fixture_dir: Path, runner: CliRunner, tmp_path: Path
) -> Generator[tuple[CliRunner, Path], None, None]:

    fixture_file = fixture_dir / "config.yaml"

    with open(fixture_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    path = tmp_path / "config.lock.json"
    data.setdefault("version", 1)
    path.write_text(json.dumps(data))

    yield runner, path

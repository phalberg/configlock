import json
import yaml
from pathlib import Path

import pytest
from typer.testing import CliRunner


@pytest.fixture
def fixture_dir():
    yield Path(__file__).resolve().parent / "test_files"


@pytest.fixture(name="runner")
def runner_setup():
    runner = CliRunner()
    yield runner


@pytest.fixture
def runner_with_lockfile(fixture_dir, runner, tmp_path):

    fixture_file = fixture_dir / "config.yaml"

    with open(fixture_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    path = tmp_path / "config.lock.json"
    data.setdefault("version", 1)
    path.write_text(json.dumps(data))

    yield runner, path


@pytest.fixture
def runner_with_lock_file_setup():
    # deprecatte this one.
    runner = CliRunner()
    with runner.isolated_filesystem():
        # initialize lock file from the repository fixture `tests/test_files/config.yaml`
        fixture = Path(__file__).resolve().parent / "test_files" / "config.yaml"

        with open(fixture, "r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh)

        # ensure lock file contains a version
        if isinstance(data, dict):
            data.setdefault("version", 1)

        with open("config.lock.json", "w", encoding="utf-8") as f:
            json.dump(data, f)
        yield runner

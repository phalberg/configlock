from pathlib import Path

from typer.testing import CliRunner
import pytest
import json


def output_debugging(result):
    print(result.exception)
    print(result.exit_code)


@pytest.fixture
def fixture_dir():
    yield Path(__file__).resolve().parent / "test_files"


@pytest.fixture
def runner_setup():
    runner = CliRunner()
    with runner.isolated_filesystem():
        yield runner


@pytest.fixture
def runner_with_file_setup():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("config.json", "w", encoding="utf-8") as f:
            json.dump({"name": "example", "object": False}, f)
        yield runner


@pytest.fixture
def runner_with_lock_file_setup():
    runner = CliRunner()
    with runner.isolated_filesystem():
        # initialize lock file from the repository fixture `tests/test_files/config.yaml`
        fixture = Path(__file__).resolve().parent / "test_files" / "config.yaml"
        import yaml

        with open(fixture, "r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh)

        # ensure lock file contains a version
        if isinstance(data, dict):
            data.setdefault("version", 1)

        with open("config.lock.json", "w", encoding="utf-8") as f:
            json.dump(data, f)
        yield runner

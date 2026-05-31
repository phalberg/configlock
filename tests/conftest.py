from typer.testing import CliRunner
import pytest
import json


def output_debbuging(result):
    print(result.exception)
    print(result.exit_code)


@pytest.fixture
def runner_setup():
    runner = CliRunner()
    with runner.isolated_filesystem():
        yield runner


@pytest.fixture
def runner_with_lock_file_setup():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("config.lock.json", "w", encoding="utf-8") as f:
            json.dump({"name": "example", "object": False}, f)
        yield runner

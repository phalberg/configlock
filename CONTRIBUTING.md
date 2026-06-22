# Contributing to ConfigLock

Thanks for helping improve ConfigLock.

## Project setup

1. Clone the repository.
2. Install dependencies:

```bash
uv sync
```

3. Run the CLI locally:

```bash
uv run configlock --help
```

## Useful commands

### Run tests

```bash
uv run pytest
```

### Lint the code

```bash
uv run ruff check src tests
```

### Format code

```bash
uv run ruff format src tests
```

## Pre-commit
Please respect the pre-commit and use it double-check that your uv is synced and that format and linting pass, please keep `--no-verify` to a minimal.

### Generate CLI docs

```bash
uv run typer cfglock.cli utils docs --output CLI.md
python scripts/merge_cli_docs.py
```

### Serve the docs locally

```bash
uv run docs-serve
```

## New versionings (only admins)
New versions to PyPi and releases can be made with the following:
1) Make a manual change to the pyproject.toml file for `version` with CORRESPONDING_NEW_VERSION (e.g say: version = "0.1.5")
2) `uv sync`
3) `git add .`
4) `git commit -m "chore: release new version"`
5) `git tag v.CORRESPONDING_NEW_VERSION`
6) `git push origin main --tags` (remember to push with the new tag(s)!)

## Development guidelines

- Keep changes focused and small when possible.
- Add or update tests when behavior changes.
- Avoid unrelated refactors in the same pull request.
- Keep command output and error messages clear and user-friendly.
- Update documentation when a change affects usage.

## Pull request checklist

- Tests pass locally.
- Linting passes locally.
- Docs are updated if needed.
- The change is described clearly in the pull request.

## Need help?

If something in the workflow is unclear, open an issue or mention it in your pull request.

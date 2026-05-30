<p align="center">
  <img src="https://github.com/phalberg/configlock/actions/workflows/ci-cd.yaml/badge.svg" alt="CI Status" />
  <img src="https://img.shields.io/badge/python-3.13-blue.svg" alt="Python Version" />
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License" />
</p>

# ConfigLock
ConfigLock is a lightweight CLI tool designed to prevent production outages by configuration errors. It brings the concept of Lockfiles (inspiration from uv) to your application’s .yaml or .json configurations.

# Quick start

```
# Clone the repo
git clone https://github.com/phalberg/configlock.git
cd configlock

# Install dependencies
uv sync

# Initialize a lockfile
uv run configlock init my_config.yaml

# Sync/Validate changes
uv run configlock sync my_config.yaml
```

If you wish to not write `uv` each time, you can do as such:

## CLI Usage

Install the project in editable mode while developing:

```bash
pip install -e .
```

Run the command directly after install:

```bash
configlock --help
configlock init {path_to_your_file}
configlock sync {path_to_your_file}
```

# Status
ConfigLock is a **personal hobby project** focused on learning robust CLI development and structural validation logic. 

> [!NOTE]
> This project is in an early prototype stage. It is a learning exercise in building developer tools with Python and Typer.

### Roadmap
- [x] Basic CLI integration with Typer
- [x] GitHub Actions CI/CD pipeline
- [x] Recursive Type & Structure checking
- [ ] GitHub API integration (Fetch remote configs)
- [ ] Web-based UI for configuration visualization

# The problem
In modern DevOps, non-technical team members often need to edit configuration files (YAML/JSON). One missing key or a wrong data type (e.g., entering a string where a boolean is expected) may crash a production environment.

# Init 
`init: Analyzes your YAML/JSON and creates a config.lock.json that stores the required structure and types.`
_Note: it will (should) only make one lock file per file path you give it._

# Sync

`sync: Compares your current YAML/JSON against the lockfile. If a key is missing or a type has changed, you get an error`

## Sync with strict ordering
Please use the command:
`configlock sync {path_to_your_file} --order-matters`
If the order of the keys matter, if not the default:
`configlock sync {path_to_your_file} --no-order-matters` 
will be set.

# License

This project is licensed under the terms of the MIT license.

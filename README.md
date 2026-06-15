<p align="center">
  <img src="https://github.com/phalberg/configlock/actions/workflows/ci-cd.yaml/badge.svg" alt="CI Status" />
  <img src="https://img.shields.io/badge/python-3.13-blue.svg" alt="Python Version" />
  <a href="https://codecov.io/github/phalberg/configlock" > 
 <img src="https://codecov.io/github/phalberg/configlock/graph/badge.svg?token=60JBRC22NB"/> 
 </a>
</p>

# ConfigLock
ConfigLock is a lightweight CLI tool designed to prevent production outages by configuration errors. It brings the concept of Lockfiles (inspiration from uv) to your application’s .yaml or .json configurations.

# Quick start

```
# Clone the repo
git clone https://github.com/phalberg/configlock
cd configlock

# Install dependencies
uv sync

# Initialize a lockfile
uv run configlock init my_config.yaml

# Sync after changes
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
```

The full command reference below is generated from [CLI.md](CLI.md) and can be refreshed with the merge script.

<!-- CLI_DOCS_START -->

# CLI

ConfigLock: Secure GitOps YAML validation engine.

**Usage**:

```console
$ [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `init`: Reads a YAML config and generates a lockfile.
* `sync`: Used to check if lock file and proposed...
* `lock`: Used to update the lock file, IF compatible

## `init`

Reads a YAML config and generates a lockfile.

**Usage**:

```console
$ init [OPTIONS] FILE_PATH
```

**Arguments**:

* `FILE_PATH`: the path for the newly proposed file  [required]

**Options**:

* `--help`: Show this message and exit.

## `sync`

Used to check if lock file and proposed file are out of sync

**Usage**:

```console
$ sync [OPTIONS] FILE_PATH
```

**Arguments**:

* `FILE_PATH`: the path for the newly proposed file  [required]

**Options**:

* `--help`: Show this message and exit.

## `lock`

Used to update the lock file, IF compatible

**Usage**:

```console
$ lock [OPTIONS] FILE_PATH
```

**Arguments**:

* `FILE_PATH`: the path for the newly proposed file  [required]

**Options**:

* `--order-matters / --no-order-matters`: choose if the order of the keys matter or not  [default: no-order-matters]
* `--help`: Show this message and exit.

<!-- CLI_DOCS_END -->

Preview the docs locally with hot reload:

```bash
uv run docs-serve
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
```bash
init: Analyzes your YAML/JSON and creates a config.lock.json that stores the required structure and types.
```
_Note: ConfigLock generates one unique lockfile corresponding to the file path provided._

# Sync

```bash
sync: Compares your current YAML/JSON against the lockfile. If a key is missing or a type has changed, you get an error.
```

# Lock
```bash
lock: Checks your current YAML/JSON and tries to replace the locked file with the new changed current file, if the change is not compatible, you get an error.

```
## Lock with strict ordering
Please use the command:
```bash
configlock lock {path_to_your_file} --order-matters
```
If the order of the keys matter, if not the default:
```bash
configlock lock {path_to_your_file} --no-order-matters
``` 
will be set.

# License

This project is licensed under the terms of the MIT license.

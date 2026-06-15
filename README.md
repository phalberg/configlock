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
# Install from PyPi
pip install cfglock

# Initialize a lockfile
configlock init my_config.yaml

# Sync after changes
configlock sync my_config.yaml
```

If you want to develop locally from the repository:

# Quick start (locally)

```bash
git clone https://github.com/phalberg/configlock
cd configlock

# Install dependencies
uv sync

# Initialize a lockfile
uv run configlock init my_config.yaml

# Sync after changes
uv run configlock sync my_config.yaml

```


If you wish to not write `uv` each time, you can do as such (editable mode):

```bash
pip install -e .
```

Run the command directly after install:

```bash
configlock --help
```

# The problem
In modern DevOps, non-technical team members often need to edit configuration files (YAML/JSON). One missing key or a wrong data type (e.g., entering a string where a boolean is expected) may crash a production environment.

<!-- CLI_DOCS_START -->

# CLI

<!-- ConfigLock: Secure GitOps YAML validation engine. -->

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


# License

This project is licensed under the terms of the MIT license.

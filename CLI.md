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

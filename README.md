# [UNDER DEVELOPMENT] Configlog
ConfigLock is a lightweight CLI tool designed to prevent production outages by configuration errors. It brings the concept of Lockfiles (heavily inspired by uv...) to your application’s .yaml configurations.

# Status
Status: Prototype __prototype__. This project is currently under heavy development - be cautions using it - fixes to certain bugs, failures and issues are being resolved - in a timely manner. 


# The problem
In modern DevOps, non-technical team members often need to edit configuration files (YAML/JSON). One missing key or a wrong data type (e.g., entering a string where a boolean is expected) may crash a production environment.

# The (underway) solution
ConfigLock acts as a Gatekeeper. It generates a "structural fingerprint" of your configuration.

`init: Analyzes your YAML/JSON and creates a config.lock.json that stores the required structure and types.`

`sync: Compares your current YAML/JSON against the lockfile. If a key is missing or a type has changed, you get an error`

# Quick start
# Clone the repo
git clone https://github.com/phalberg/configlock.git
cd configlock

# Install dependencies
uv sync

# Initialize a lockfile
uv run configlock init my_config.yaml

# Sync/Validate changes
uv run configlock sync my_config.yaml


## CLI Usage

Install the project in editable mode while developing:

```bash
pip install -e .
```

Run the command directly after install:

```bash
configlock --help
configlock init tests/test_files/config.yaml
configlock sync tests/test_files/config.yaml
```

You can also run the package module directly:

```bash
python -m configlock init tests/test_files/config.yaml
```

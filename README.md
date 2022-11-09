# Autonity CLI

A command-line RPC client for Autonity.  Run `aut --help` for the list of all commands and options.

## Quick Start

### Installation

You need python >=3.7 with [pipx](https://pypa.github.io/pipx/) installed. The command can then be installed as a pipx package isolated in its own environment.

```console
$ git clone --recurse-submodules https://github.com/autonity/autcli
$ cd autcli
$ make install
```

### Usage

The `aut` command should now be available like any other unix command.  Use `aut` by itself to list commands and `aut <command> -h` to get help for individual commands.

### `.autrc` files

This (optional) file set configuration parameters, which can be overridden by environment variables and command-line parameters.  See the [sample file](.autrc.sample) in this repo.

If `.autrc` is not found in the current directory, all parent directories are searched in turn and the first `.autrc` file found is used.

## Development

The [autonity.py](https://github.com/autonity/autonity.py) dependency
is included as a submodule, for ease of development  To sync the submodules:
```console
$ git submodule update --init --recursive
```

Create and activate a virtual-env:
```console
$ python -m venv env
$ . env/bin/activate
```

(Note the `(env)` prefix to your prompt.  Activate the venv from other
terminals using the same `. env/bin/activate` command.)

Install both `autetl` and `autonity.py` in "editable" mode, within this virtual-env:
development:
```console
(env)$ make
```

(Note that the `aut` command is also installed in the virtual-env.)

Execute all code checks (linters, type-checker, unit tests, etc):
```console
(env)$ make check
```

Some tests scripts (which invoke the `aut` command itself) are available in the [scripts](./scripts) directory.  The are intended to be run within the virtual-env, from the repository root directory.

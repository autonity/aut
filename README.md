# Autonity CLI

A command-line RPC client for Autonity.  Run `aut --help` for the list
of all commands and options.

Currently implements only a subset of generic Web3 functionality, but
will be expanded in functionality to cover the entire
autonity-specific RPC namespace as well,

## Installation

You need python >=3.7 with [pipx](https://pypa.github.io/pipx/)
installed. Clone the repo and submodules and `make install`.

pipx will install autcli in a virtual environment, but provide `aut`
as a console entry point that is globally available on your system
like any other unix command. This achieves isolation without the user
needing to know anything about python venv usage.. or python itself,
for that matter.

## `.autrc` files

This (optional) file can store configuration information, which can be overridden by environment variables and command-line parameters.  See the [sample file](.autrc.sample) in this repo.

If `.autrc` is not found in the current directory, all parent directories are searched in turn and the first `.autrc` file found is used.

## Installation for development

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

The `aut` command is now available to any console with the virtual-env
activated.

Execute all code checks (linters, type-checker, unit tests, etc):
```console
(env)$ make check
```

Some tests scripts (which invoke the `aut` command itself) are available in the [scripts](./scripts) directory.  The are intended to be run within the virtual-env, from the repository root directory.

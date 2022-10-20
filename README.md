# Autonity CLI

A command-line RPC client for Autonity.

```
$ aut --help
Autonity RPC Client

Usage:
  aut [options] [<command>] [<args>...]

Options:
  -h, --help               show this screen.
  --version                show version.

System Commands:
  list       list local keyfile information, aut commands.

Web3 Commands:
  get        get block, account, transaction or node information from an RPC server.
  maketx     specify transaction data, print json output.
  signtx     sign transaction data, print raw transaction bytes.
  sendtx     send a raw transaction bytes to the network.

Autonity Commands:

  TODO - CLI INTERFACES FOR ALL AUTONITY-SPECIFIC RPC METHODS

See 'aut <command> --help' for more information on a specific command.

By default the RPC endpoint is 'http://localhost:8545'. If your http
endpoint is different, or you are using websockets or IPC, you need to
define it in your shell like 'export WEB3_PROVIDER=<your-endpoint>`.
```

Currently implements only a subset of generic Web3 functionality, but
the idea would be to expand functionality to cover the entire
autonity-specific RPC namespace as well,

## Installation

You need python >=3.7 with [pipx](https://pypa.github.io/pipx/)
installed. Clone the repo and `make install`.

pipx will install autcli in a virtual environment, but provide `aut`
as a console entry point that is globally available on your system
like any other unix command. This achieves isolation without the user
needing to know anything about python venv usage.. or python itself,
for that matter.

## Tests

Run `make tests`. Only a tiny set of unit tests exist right now.

I'm not python programmer and don't know how to best test a python
_command-line_ program. There are a couple of non-standard aspects
AFAICT:

- I guess tests should really replicate `aut` shell invocations with
  its stdtin, stdout, etc.

- Most of the usage involves RPC calls, so there's integration
  involved.

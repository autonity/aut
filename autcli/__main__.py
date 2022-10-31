"""Autonity RPC Client

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
"""

from autcli.commands import maketx, signtx, sendtx, waittx

from click import group


@group()
def aut() -> None:
    """
    Command line interface to Autonity functionality.
    """


aut.add_command(maketx.maketx)
aut.add_command(signtx.signtx)
aut.add_command(sendtx.sendtx)
aut.add_command(waittx.waittx)

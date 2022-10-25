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

from autonity import Autonity
from autcli.constants import UnixExitStatus
from autcli.commands import get, list, maketx, signtx, sendtx
from autcli import __version__
from autcli import __file__

from click import group
from docopt import docopt
import os
import sys
from schema import Schema, SchemaError, Or


@group()
def aut() -> None:
    """
    Command line interface to Autonity functionality.
    """
    pass


aut.add_command(maketx.maketx)
aut.add_command(signtx.signtx)


# def cli():
#     argv = sys.argv
#     del argv[0]
#     aut_(argv)


# def aut_(argv):
#     """
#     This function is called every time that 'aut' is run from the
#     command line. If user provides sub-command, this function will
#     dispatch the corresponding function in the autcli.commands
#     submodule. The command line arguments are passed as a dictionary.
#     """
#     args = docopt(__doc__, version=__version__, argv=argv, options_first=True)
#     pkg_path = os.path.dirname(__file__)
#     argv = [args["<command>"]] + args["<args>"]
#     del args["<args>"]
#     s = Schema(
#         {
#             "<command>": lambda cmd: os.path.exists(pkg_path + f"/commands/{cmd}.py"),
#             "--version": Or(True, False),
#             "--help": Or(True, False),
#         }
#     )
#     try:
#         args = s.validate(args)
#     except SchemaError:
#         cmd = args["<command>"]
#         print(f"{cmd} is not a valid command. see 'aut --help'")
#         sys.exit(UnixExitStatus.CLI_INVALID_OPTION_VALUE)
#     if args["<command>"] == "get":
#         rtn = get.aut_get(argv)
#     if args["<command>"] == "list":
#         rtn = list.aut_list(argv)
#     if args["<command>"] == "maketx":
#         rtn = maketx.aut_maketx(argv)
#     if args["<command>"] == "signtx":
#         rtn = signtx.aut_signtx(argv)
#     if args["<command>"] == "sendtx":
#         rtn = sendtx.aut_sendtx(argv)
#     sys.exit(rtn)


# if __name__ == "__main__":
#     sys.exit(cli())

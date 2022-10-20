"""
Code that is executed when 'aut sendtx..' is invoked on the command-line.
"""
from docopt import docopt
from schema import Schema, SchemaError, Or
import sys
from autcli.constants import UnixExitStatus
from autcli.user import sendtx
from autcli import __version__
from autcli import __file__


def aut_sendtx(argv):
    """
    Usage:
      aut sendtx [options]

    Options:
      --debug       if set, errors will print traceback along with exception msg.
      -h --help     show this screen.

    Send to the network raw transaction bytes on the stdin via eth_sendRawTransaction.
    """
    try:
        args = docopt(aut_sendtx.__doc__, version=__version__, argv=argv)
    except:
        print(aut_sendtx.__doc__)
        return UnixExitStatus.CLI_INVALID_INVOCATION
    if not args["--debug"]:
        sys.tracebacklimit = 0
    del args["sendtx"]
    s = Schema(
        {
            "--help": Or(True, False),
            "--debug": Or(True, False),
        }
    )
    try:
        args = s.validate(args)
    except SchemaError as exc:
        print(exc.code)
        return UnixExitStatus.CLI_INVALID_OPTION_VALUE
    args = s.validate(args)
    rawtxs = sys.stdin.read().splitlines()
    for tx_raw in rawtxs:
        tx_hash = sendtx(tx_raw)
        print(tx_hash.hex())
    return 0

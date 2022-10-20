"""
Code that is executed when 'aut signtx..' is invoked on the command-line.
"""
from docopt import docopt
import os
import sys
import json
from getpass import getpass
from autcli.constants import UnixExitStatus
from autcli.user import client_signtx, server_signtx
from autcli import __version__
from autcli import __file__
from schema import Schema, SchemaError, Or, Use


def aut_signtx(argv):
    """Usage:
      aut signtx --client-sign [--keystore DIR] [options]
      aut signtx --server-sign [options]

    Signing options:
      --client-sign   client-sign the transaction data using a local KEYFILE.
      --server-sign   server-sign the transaction data using node account via RPC.
      --keystore DIR  local keystore directory [default: ~/.autonity/keystore].

    Other options:
      --debug         if set, errors will print traceback as well as exception.
      -h --help       show this screen.

    USE --server-sign ONLY IF YOU CONTROL YOUR RPC ENDPOINT AND UNDERSTAND THE SECURITY
    IMPLICATIONS OF HOSTING ACCOUNTS ON A NODE. The recommended approach is to sign your
    tx's locally with --client-sign.

    When using --client-sign, aut will first try to read the keyfile password from
    environment variable 'KEYFILEPWD' (set it like 'export KEYFILEPWD=<password>'), and
    if that's not defined it will prompt you for it.
    """
    try:
        args = docopt(aut_signtx.__doc__, version=__version__, argv=argv)
    except:
        print(aut_signtx.__doc__)
        return UnixExitStatus.CLI_INVALID_INVOCATION
    if not args["--debug"]:
        sys.tracebacklimit = 0
    del args["signtx"]
    s = Schema(
        {
            "--client-sign": Or(True, False),
            "--server-sign": Or(True, False),
            "--keystore": Or(None, Use(os.path.expanduser)),
            "--debug": Or(True, False),
            "--help": Or(True, False),
        }
    )
    try:
        args = s.validate(args)
    except SchemaError as exc:
        print(exc.code)
        return UnixExitStatus.CLI_INVALID_OPTION_VALUE

    txs = sys.stdin.read().splitlines()
    for tx in txs:
        tx = json.loads(tx)
        if args["--client-sign"]:
            keyfile_pass = os.getenv("KEYFILEPWD")
            if keyfile_pass is None:
                try:
                    acct = tx["from"]
                    keyfile_pass = getpass(
                        "Environment variable KEYFILEPWD is not set."
                        + "Consider doing 'export KEYFILEPWD=<password>'."
                        + f"\nEnter passphrase for {acct} (or CTRL-d to exit): "
                    )
                except EOFError:
                    print("\n")
                    return None
            tx_signed = client_signtx(tx, args["--keystore"], keyfile_pass)
            print(tx_signed.rawTransaction.hex())
        elif args["--server-sign"]:
            tx_signed = server_signtx(tx)
            print(tx_signed.hex())
    return 0


# Other Features Contemplated
# ===========================
#
# Hardware Wallets
# ----------------
#
# extend client-signing usage like:
#
#  --trezor-sign    client-sign the transaction data using a trezor device.
#  --ledger-sign    client-sign the transaction data using a ledger device.
#
# trezor has a first-party python library, should be straightforward
# - https://pypi.org/project/trezor/
# - https://stackoverflow.com/questions/63608705/send-signed-transaction-from-trezor-hardware-wallet
#
# ledger looks like hard work via third-party solutions
# - https://pypi.org/project/ledgereth/ (BETA!)
# - https://gist.github.com/bargst/5f896e4a5984593d43f1b4eb66f79d68
# - https://github.com/ethereum/eth-account/issues/25
#
# but ledger recently open sourced their own, so maybe not too hard?
# - https://github.com/LedgerHQ/ledgerctl

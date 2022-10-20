"""
Code that is executed when 'aut get..' is invoked on the command-line.
"""
from docopt import docopt
from autcli.utils import (
    to_checksum_address,
    to_json,
    validate_block_identifier,
    validate_32byte_hash_string,
)
from autcli.user import (
    get_account_stats,
    get_node_stats,
    get_block,
    get_transaction_receipt,
)
from autcli.constants import UnixExitStatus
from autcli import __version__
from autcli import __file__
from schema import Schema, SchemaError, Or, Use
import sys


def aut_get(argv):
    """
    Usage:
      aut get stats [options]
      aut get block <identifier> [options]
      aut get account (<address>... | --stdin) [--asof TAG] [options]
      aut get receipt (<tx-hash>... | --stdin) [--wait INT] [options]

    Commands:
      stats        print general stats about RPC node and the blockchain it's on.
      block        print information for block, where <identifier> is a block number or hash.
      account      print account tx count and balance state of one or more accounts.
      receipt      print receipt for one or more tx hashes.

    Options:
      --asof TAG   state as of TAG, one of block number, 'latest', 'earliest', or 'pending'.
      --wait INT   wait INT seconds for tx to get mined before responding TransactionNotFound [default: 0]
      --stdin      read account lines from stdin instead of positional arguments.
      --debug      if set, errors will print traceback along with exception msg.
      -h --help    show this screen.
    """
    try:
        args = docopt(aut_get.__doc__, version=__version__, argv=argv)
    except:
        return UnixExitStatus.CLI_INVALID_INVOCATION
    if not args["--debug"]:
        sys.tracebacklimit = 0
    del args["get"]
    s = Schema(
        {
            "stats": Or(True, False),
            "block": Or(True, False),
            "account": Or(True, False),
            "receipt": Or(True, False),
            "--asof": Or(
                None,
                "latest",
                "earliest",
                "pending",
                error="--asof must be one of 'latest', 'earliest' or 'pending'",
            ),
            "--wait": Use(int),
            "--stdin": Or(True, False),
            "--debug": Or(True, False),
            "--help": Or(True, False),
            "<identifier>": Or(
                None,
                Use(
                    validate_block_identifier,
                    error="<identifier> is not a block number or a valid 32-byte block hash",
                ),
            ),
            "<address>": Or(
                [],
                Use(
                    lambda x: list(map(to_checksum_address, x)),
                    error="<address> is not a valid address",
                ),
            ),
            "<tx-hash>": Or(
                [],
                Use(
                    lambda x: list(map(validate_32byte_hash_string, x)),
                    error="<tx-hash> is not a valid hash",
                ),
            ),
        }
    )
    try:
        args = s.validate(args)
    except SchemaError as exc:
        print(exc.code)
        return UnixExitStatus.CLI_INVALID_OPTION_VALUE

    if args["stats"]:
        stats = get_node_stats()
        print(to_json(stats))
    elif args["block"]:
        blk = get_block(args["<identifier>"])
        print(to_json(blk))
    elif args["account"]:
        if args["--asof"] is not None:
            tag = args["--asof"]
        else:
            tag = None
        if args["--stdin"]:
            accounts = sys.stdin.read().splitlines()
        else:
            accounts = args["<address>"]
        account_stats = get_account_stats(accounts, tag)
        for acct in account_stats.keys():
            print(
                acct
                + " "
                + str(account_stats[acct][0])
                + " "
                + str(account_stats[acct][1])
            )
    elif args["receipt"]:
        if args["--stdin"]:
            hashes = sys.stdin.read().splitlines()
        else:
            hashes = args["<tx-hash>"]
        for h in hashes:
            tx_receipt = get_transaction_receipt(h, args["--wait"])
            print(to_json(tx_receipt))
    return 0

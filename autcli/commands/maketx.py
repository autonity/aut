"""
Code that is executed when 'aut maketx..' is invoked on the command-line.
"""
from docopt import docopt
from autcli.user import (
    get_account_transaction_count,
    get_block,
    get_latest_block_number,
)
from autcli.constants import UnixExitStatus
from autcli.utils import to_checksum_address, to_json, parse_wei_representation
from autcli import __version__
from autcli import __file__
from schema import Schema, SchemaError, And, Or, Use
import sys
from web3 import Web3


def aut_maketx(argv):
    """
    Usage:
      aut maketx -f ADR -t ADR -g INT -P WEI [-d HEX | -] [options]
      aut maketx --legacy -f ADR -t ADR -g INT -p WEI [-d HEX | -] [options]

    Options:
      -f ADR --from=ADR                 address from which tx is sent.
      -t ADR --to=ADR                   address to which tx is directed.
      -g INT --gas=INT                  maximum gas units that can be consumed by the tx.
      -p WEI --gasPrice=WEI             value per gas to (legacy, use -F and -P instead).
      -P WEI --maxPriorityFeePerGas=WEI maximum willing to pay per gas as tip to block proposer.
      -F WEI --maxFeePerGas=WEI         maximum willing to pay per gas for the total fee of the tx.
      -n INT --nonce=INT                tx nonce; query chain for account tx count if not given.
      -v WEI --value=WEI                value sent with tx (nb '7000000000' and '7gwei' are identical).
      -d HEX --data=HEX                 compiled contract code OR method signature and parameters.
      -I INT --chainId=INT              integer representing EIP155 chainId [default: 65010000].
      --fee-factor NUM                  set maxFeePerGas to last block's basefee x NUM [default: 2].
      --legacy                          if set, tx type is 0x0 (pre-EIP1559), otherwise type is 0x2.
      --debug                           if set, errors will print traceback along with exception msg.
      -h --help                         show this screen.
    """
    try:
        args = docopt(aut_maketx.__doc__, version=__version__, argv=argv)
    except:
        print(aut_maketx.__doc__)
        return UnixExitStatus.CLI_INVALID_INVOCATION
    if not args["--debug"]:
        sys.tracebacklimit = 0
    del args["maketx"]
    s = Schema(
        {
            "--from": Use(
                Web3.toChecksumAddress, error="-f, --from: not a valid address format"
            ),
            "--to": Use(
                Web3.toChecksumAddress, error="-t, --to: not a valid address format"
            ),
            "--nonce": Or(
                None,
                And(lambda n: n.isnumeric(), lambda n: int(n) > 0),
                error="invalid nonce",
            ),
            "--gas": And(
                lambda n: n.isnumeric(), lambda n: int(n) > 0, error="invalid gas value"
            ),
            "--gasPrice": Or(
                None,
                Use(parse_wei_representation),
                error="-p, --gasPrice: cannot convert to integer",
            ),
            "--maxFeePerGas": Or(
                None,
                Use(parse_wei_representation),
                error="-F, --maxFeePerGas: cannot convert to integer",
            ),
            "--maxPriorityFeePerGas": Or(
                None,
                Use(parse_wei_representation),
                error="-P, --maxPriorityFeePerGas: cannot convert to integer",
            ),
            "--value": Or(
                None,
                Use(parse_wei_representation),
                error="-v, --value: cannot convert to integer",
            ),
            "--data": Or(None, Use(str)),
            "--chainId": And(lambda n: n.isnumeric(), lambda n: int(n) > 0),
            "--fee-factor": And(lambda n: n.isnumeric(), lambda n: float(n) > 0),
            "--legacy": Or(True, False),
            "--debug": Or(True, False),
            "--help": Or(True, False),
            "-": Or(True, False),
        }
    )
    try:
        args = s.validate(args)
    except SchemaError as exc:
        print(exc)
        return UnixExitStatus.CLI_INVALID_OPTION_VALUE

    if args["--nonce"] is None:
        nonce = get_account_transaction_count(args["--from"])
    else:
        nonce = int(args["--nonce"])

    args["--gas"] = int(args["--gas"])

    if args["--gasPrice"] is not None:
        args["--gasPrice"] = int(args["--gasPrice"])

    args["--fee-factor"] = float(args["--fee-factor"])

    if args["--maxFeePerGas"] is None:
        block_number = get_latest_block_number()
        block_data = get_block(block_number)
        max_fee_per_gas = float(block_data["baseFeePerGas"]) * args["--fee-factor"]
        max_fee_per_gas = int(max_fee_per_gas)
    else:
        max_fee_per_gas = int(args["--maxFeePerGas"])

    if args["--maxPriorityFeePerGas"] is not None:
        args["--maxPriorityFeePerGas"] = int(args["--maxPriorityFeePerGas"])

    if args["--value"] is not None:
        args["--value"] = int(args["--value"])

    args["--chainId"] = int(args["--chainId"])

    if args["-"]:
        if args["--data"] is not None:
            print("ignoring value passed to --data because data found on stdin.")
        data = sys.stdin.read().splitlines()
        data = data[0]
        args["--data"] = data

    if args["--legacy"]:
        erc2718_type = "0x0"
    else:
        erc2718_type = "0x2"

    tx = {
        "from": args["--from"],
        "to": args["--to"],
        "nonce": nonce,
        "gas": args["--gas"],
        "gasPrice": args["--gasPrice"],
        "maxFeePerGas": max_fee_per_gas,
        "maxPriorityFeePerGas": args["--maxPriorityFeePerGas"],
        "value": args["--value"],
        "data": args["--data"],
        "chainId": args["--chainId"],
        "type": erc2718_type,
    }

    tx = {k: v for k, v in tx.items() if v is not None}

    print(to_json(tx))

    return 0


# Other Features Contemplated
# ===========================
#
# Typed Transactions
# ------------------
#
# - https://eips.ethereum.org/EIPS/eip-2718
# E.g., support for transactions with access lists, etc.

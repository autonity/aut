"""
Code that is executed when 'aut maketx..' is invoked on the command-line.
"""
from autcli.user import (
    get_account_transaction_count,
    get_block,
    get_latest_block_number,
)
from autcli.utils import parse_wei_representation, to_json
from autcli import __version__
from autcli import __file__

from web3 import Web3
from web3.types import TxParams, Nonce, Wei, HexStr
from click import command, option, ClickException
from typing import Dict, Optional, Any, cast

# pylint: disable=too-many-locals
# pylint: disable=too-many-arguments
# pylint: disable=too-many-branches


@command()
@option("--from", "-f", "from_str", help="address from which tx is sent.")
@option("--to", "-t", "to_str", help="address to which tx is directed.")
@option(
    "--gas",
    "-g",
    required=True,
    help="maximum gas units that can be consumed by the tx.",
)
@option(
    "--gas-price",
    "-p",
    help="value per gas (legacy, use -F and -P instead).",
)
@option(
    "--max-priority-fee-per-gas",
    "-P",
    help="maximum to pay per gas as tip to block proposer.",
)
@option(
    "--max-fee-per-gas",
    "-F",
    help="maximum to pay per gas for the total fee of the tx.",
)
@option(
    "--nonce",
    "-n",
    type=int,
    help="tx nonce; query chain for account tx count if not given.",
)
@option(
    "--value",
    "-v",
    help="value sent with tx (nb '7000000000' and '7gwei' are identical).",
)
@option(
    "--data", "-d", help="compiled contract code OR method signature and parameters."
)
@option(
    "--chain-id",
    "-I",
    type=int,
    help="integer representing EIP155 chainId [default: 65010000].",
)
@option(
    "--fee-factor",
    type=float,
    help="set maxFeePerGas to <last-basefee> x <fee-factor> [default: 2].",
)
@option(
    "--legacy",
    is_flag=True,
    help="if set, tx type is 0x0 (pre-EIP1559), otherwise type is 0x2.",
)
def maketx(
    from_str: Optional[str],
    to_str: Optional[str],
    gas: Optional[str],
    gas_price: Optional[str],
    max_priority_fee_per_gas: Optional[str],
    max_fee_per_gas: Optional[str],
    nonce: Optional[int],
    value: Optional[str],
    data: Optional[str],
    chain_id: Optional[int],
    fee_factor: Optional[float],
    legacy: bool,
) -> None:
    """
    Create a transaction given the parameters passed in.
    """

    from_addr = Web3.toChecksumAddress(from_str) if from_str else None
    to_addr = Web3.toChecksumAddress(to_str) if to_str else None

    tx: TxParams = {}

    # Must have the nonce to put into the tx, or the from_addr to
    # compute it from.

    if not nonce:
        if not from_addr:
            raise ClickException("must specify either --nonce or --from")
        nonce = get_account_transaction_count(from_addr)
    tx["nonce"] = Nonce(nonce)

    if from_addr:
        tx["from"] = from_addr

    if to_addr:
        tx["to"] = to_addr

    if gas:
        tx["gas"] = parse_wei_representation(gas)

    # Require either gas_price OR max_fee_per_gas, etc

    if gas_price:
        if fee_factor or fee_factor or max_fee_per_gas or max_priority_fee_per_gas:
            raise ClickException("--gas-price cannot be used with other fee parameters")
        tx["gasPrice"] = parse_wei_representation(gas_price)
    else:
        if max_fee_per_gas:
            tx["maxFeePerGas"] = max_fee_per_gas
        elif fee_factor:
            block_number = get_latest_block_number()
            block_data = get_block(block_number)
            tx["maxFeePerGas"] = Wei(
                int(float(block_data["baseFeePerGas"]) * fee_factor)
            )
        else:
            raise ClickException(
                "must specify one of --max-fee-per-gas or --fee-factor"
            )

        if max_priority_fee_per_gas:
            tx["maxPriorityFeePerGas"] = max_priority_fee_per_gas
        else:
            tx["maxPriorityFeePerGas"] = tx["maxFeePerGas"]

    # Value

    if value:
        tx["value"] = parse_wei_representation(value)
    elif not data:
        raise ClickException("Empty tx (neither value or data given)")

    # Data

    if data:
        tx["data"] = HexStr(data)

    # Chain ID

    if chain_id:
        tx["chainId"] = chain_id

    # If the --legacy flag was given, explicitly set the type,
    # otherwise have web3 determine it.

    if legacy:
        tx["type"] = HexStr("0x0")

    print(to_json(cast(Dict[Any, Any], tx)))


# Other Features Contemplated
# ===========================
#
# Typed Transactions
# ------------------
#
# - https://eips.ethereum.org/EIPS/eip-2718
# E.g., support for transactions with access lists, etc.

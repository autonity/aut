"""
Code that is executed when 'aut maketx..' is invoked on the command-line.
"""

from autcli.logging import log
from autcli.options import rpc_endpoint_option, newton_or_token_option, keyfile_option
from autcli.utils import (
    create_tx_from_args,
    finalize_tx_from_args,
    create_contract_tx_from_args,
    parse_wei_representation,
    to_json,
    web3_from_endpoint_arg,
    from_address_from_argument_optional,
    newton_or_token_to_address,
)

from autonity.erc20 import ERC20

from web3 import Web3
from web3.types import Wei, HexStr
from click import command, option, ClickException
from typing import Optional

# pylint: disable=too-many-locals
# pylint: disable=too-many-arguments
# pylint: disable=too-many-branches
# pylint: disable=too-many-statements


@command()
@rpc_endpoint_option
@newton_or_token_option
@keyfile_option()
@option(
    "--from",
    "-f",
    "from_str",
    help="address from which tx is sent (extracted from keyfile if not given).",
)
@option("--to", "-t", "to_str", help="address to which tx is directed.")
@option(
    "--gas",
    "-g",
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
    required=True,
    help="value sent with tx (nb '7000000000' and '7gwei' are identical).",
)
@option(
    "--data", "-d", help="compiled contract code OR method signature and parameters."
)
@option(
    "--chain-id",
    "-I",
    type=int,
    help="integer representing EIP155 chainId.",
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
    rpc_endpoint: Optional[str],
    ntn: bool,
    token: Optional[str],
    key_file: Optional[str],
    from_str: Optional[str],
    to_str: Optional[str],
    gas: Optional[str],
    gas_price: Optional[str],
    max_priority_fee_per_gas: Optional[str],
    max_fee_per_gas: Optional[str],
    nonce: Optional[int],
    value: str,
    data: Optional[str],
    chain_id: Optional[int],
    fee_factor: Optional[float],
    legacy: bool,
) -> None:
    """
    Create a transaction given the parameters passed in.
    """

    # TODO: Add a flag which results in only unconnected Web3
    # instances being created.  Callers who do not want to connect to
    # a node will then receive an error if they do not specify some
    # missing value (rather than having Web3.py silently connect for
    # them).

    # Potentially used in multiple places, so avoid re-initializing.
    w3: Optional[Web3] = None

    # If from_str is not set, take the address from a keyfile instead
    # (if given)
    from_addr = from_address_from_argument_optional(from_str, key_file)
    log(f"from_addr: {from_addr}")

    to_addr = Web3.toChecksumAddress(to_str) if to_str else None

    if to_addr is None:
        raise ClickException(
            "to-address must be specified.  (contract deployment not yet supported)"
        )

    token_addresss = newton_or_token_to_address(ntn, token)

    # If --fee-factor was given, we must do some computation up-front

    if fee_factor:
        w3 = web3_from_endpoint_arg(w3, rpc_endpoint)
        block_number = w3.eth.block_number
        block_data = w3.eth.get_block(block_number)
        max_fee_per_gas = str(Wei(int(float(block_data["baseFeePerGas"]) * fee_factor)))

    # If this is a token call, fill in the "to" and "data" fields
    # using the contract call.  Otherwise, for a plain AUT transfer,
    # use create_transaction and finalize_transaction wrappers.

    if token_addresss:

        if not from_addr:
            raise ClickException("from address not given")

        w3 = web3_from_endpoint_arg(w3, rpc_endpoint)
        function = ERC20(w3, token_addresss).transfer(
            recipient=to_addr, amount=parse_wei_representation(value)
        )
        tx = create_contract_tx_from_args(
            function=function,
            from_addr=from_addr,
            gas=gas,
            gas_price=gas_price,
            max_fee_per_gas=max_fee_per_gas,
            max_priority_fee_per_gas=max_priority_fee_per_gas,
            nonce=nonce,
            chain_id=chain_id,
        )

    else:

        if not from_addr:
            raise ClickException("from address not given")

        if not value and not data:
            raise ClickException("Empty tx (neither value or data given)")

        tx = create_tx_from_args(
            from_addr=from_addr,
            to_addr=to_addr,
            value=value,
            data=data,
            gas=gas,
            gas_price=gas_price,
            max_fee_per_gas=max_fee_per_gas,
            max_priority_fee_per_gas=max_priority_fee_per_gas,
            nonce=nonce,
            chain_id=chain_id,
        )

        # Fill in any missing values.

        tx = finalize_tx_from_args(w3, rpc_endpoint, tx, from_addr)

    # If the --legacy flag was given, explicitly set the type,
    # otherwise have web3 determine it.

    if legacy:
        tx["type"] = HexStr("0x0")

    print(to_json(tx))


# Other Features Contemplated
# ===========================
#
# Typed Transactions
# ------------------
#
# - https://eips.ethereum.org/EIPS/eip-2718
# E.g., support for transactions with access lists, etc.

"""
Code that is executed when 'aut maketx..' is invoked on the command-line.
"""

from autcli.logging import log
from autcli.options import rpc_endpoint_option, newton_or_token_option, keyfile_option
from autcli.utils import (
    parse_wei_representation,
    to_json,
    web3_from_endpoint_arg,
    newton_or_token_to_address,
)
from autcli import config

from autonity.erc20 import ERC20
from autonity.utils.keyfile import load_keyfile, get_address_from_keyfile

from web3 import Web3
from web3.types import TxParams, Nonce, Wei, HexStr, ChecksumAddress
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
    value: Optional[str],
    data: Optional[str],
    chain_id: Optional[int],
    fee_factor: Optional[float],
    legacy: bool,
) -> None:
    """
    Create a transaction given the parameters passed in.
    """

    # TODO: function is too big.  break into smaller pieces.

    # Potentially used in multiple places, so avoid re-initializing.
    w3: Optional[Web3] = None

    # If from_str is not set, take the address from a keyfile instead
    # (if given)
    if from_str:
        from_addr: Optional[ChecksumAddress] = Web3.toChecksumAddress(from_str)
    else:
        log("no from-addr given.  attempting to extract from keyfile")
        key_file = config.get_keyfile_optional(key_file)
        if key_file:
            key_data = load_keyfile(key_file)
            from_addr = get_address_from_keyfile(key_data)
            log(f"got keyfile: {key_file}, address: {from_addr}")
        else:
            log("no keyfile.  empty from-addr")
            from_addr = None
    log(f"from_addr: {from_addr}")

    to_addr = Web3.toChecksumAddress(to_str) if to_str else None

    if to_addr is None:
        raise ClickException(
            "to-address must be specified.  (contract deployment not yet supported)"
        )

    token_addresss = newton_or_token_to_address(ntn, token)

    tx: TxParams

    if token_addresss:
        # Create TxParams using the contract call.  We must have a
        # from-address and value, and data should be set.
        if from_addr is None:
            raise ClickException("from-address required for token transfers")
        if not value:
            raise ClickException("value is required for token transfers")
        if data:
            raise ClickException("data cannot be set for token transfers")

        # TODO: check contract for number of decimals.  For now, use
        # the auton denominations everywhere.

        # TODO: this currently requires a Web3 connection in order to
        # estimate gas, gas price, nonce, and chainId .  At least for
        # NTN, this should all be known and we should be able to do
        # this offline.

        w3 = web3_from_endpoint_arg(w3, rpc_endpoint)
        tx = ERC20(w3, token_addresss).transfer(
            from_addr,
            to_addr,
            parse_wei_representation(value),
            Wei(int(gas)) if gas else Wei(0),
            Wei(int(gas_price)) if gas_price else Wei(0),
            Nonce(nonce) if nonce else Nonce(0),
        )

    else:

        # Create a simple tx with optional data
        tx = {}
        if from_addr:
            tx["from"] = Web3.toChecksumAddress(from_addr)

        if to_addr:
            tx["to"] = Web3.toChecksumAddress(to_addr)

        if value:
            tx["value"] = parse_wei_representation(value)
        elif not data:
            raise ClickException("Empty tx (neither value or data given)")

        if gas:
            tx["gas"] = parse_wei_representation(gas)
        else:
            w3 = web3_from_endpoint_arg(w3, rpc_endpoint)
            tx["gas"] = w3.eth.estimateGas(tx)

        # Data
        if data:
            tx["data"] = HexStr(data)

    # Must have the nonce to put into the tx, or the from_addr to
    # compute it from.

    if not nonce:
        if not from_addr:
            raise ClickException("must specify either --nonce or --from")

        w3 = web3_from_endpoint_arg(w3, rpc_endpoint)
        nonce = w3.eth.get_transaction_count(from_addr)
    tx["nonce"] = Nonce(nonce)

    # Require either gas_price OR max_fee_per_gas, etc

    if gas_price:
        if fee_factor or fee_factor or max_fee_per_gas or max_priority_fee_per_gas:
            raise ClickException("--gas-price cannot be used with other fee parameters")
        tx["gasPrice"] = parse_wei_representation(gas_price)
    else:
        if max_fee_per_gas:
            tx["maxFeePerGas"] = str(max_fee_per_gas)
        elif fee_factor:
            w3 = web3_from_endpoint_arg(w3, rpc_endpoint)
            block_number = w3.eth.block_number
            block_data = w3.eth.get_block(block_number)
            tx["maxFeePerGas"] = str(
                Wei(int(float(block_data["baseFeePerGas"]) * fee_factor))
            )
        else:
            raise ClickException(
                "must specify one of --max-fee-per-gas or --fee-factor"
            )

        if max_priority_fee_per_gas:
            tx["maxPriorityFeePerGas"] = str(max_priority_fee_per_gas)
        else:
            tx["maxPriorityFeePerGas"] = tx["maxFeePerGas"]

    # Chain ID

    if chain_id:
        tx["chainId"] = chain_id
    else:
        w3 = web3_from_endpoint_arg(w3, rpc_endpoint)
        tx["chainId"] = w3.eth.chain_id

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

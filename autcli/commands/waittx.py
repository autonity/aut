"""
The waittx command.
"""

from autcli.options import rpc_endpoint_option
from autcli.utils import web3_from_endpoint_arg, to_json, validate_32byte_hash_string


from autonity.utils.tx import wait_for_tx

import asyncio
from web3.types import HexBytes
from click import ClickException, command, option, argument
from typing import Optional


@command()
@rpc_endpoint_option
@option("--quiet", "-q", is_flag=True, help="Do not dump the full transaction receipt.")
@option(
    "--timeout",
    "-t",
    type=float,
    help="Wait up to some (non-whole) number of seconds.",
)
@argument("tx-hash", required=True)
def waittx(
    rpc_endpoint: Optional[str], quiet: bool, timeout: Optional[float], tx_hash: str
) -> None:
    """
    Wait for a transaction with a specific hash, and dump the receipt.
    The command will return exit code 0 if the transaction
    succeeded, or non-zero otherwise.

    Timeouts also result in a non-zero exit code.
    """

    hash_bytes = HexBytes(validate_32byte_hash_string(tx_hash))

    try:
        w3 = web3_from_endpoint_arg(None, rpc_endpoint)
        tx_receipt = wait_for_tx(w3, hash_bytes, timeout=timeout)
        if not quiet:
            print(to_json(tx_receipt))

        if tx_receipt["status"] == 0:
            raise ClickException("Transaction failed")

    except asyncio.TimeoutError:
        raise ClickException(  # pylint: disable=raise-missing-from
            "Tx {tx_hash} timed out"
        )

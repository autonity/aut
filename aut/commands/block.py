"""
The "block" command group
"""

from click import argument, command, group
from web3 import Web3

from ..options import config_option, rpc_endpoint_option
from ..user import get_block
from ..utils import to_json, validate_block_identifier


@group(name="block")
def block_group() -> None:
    """Commands for querying block information."""


@command()
@config_option
@rpc_endpoint_option
@argument("identifier", default="latest")
def get(w3: Web3, identifier: str) -> None:
    """Print information for block.

    IDENTIFIER is a block number or hash. If no argument is given, "latest" is used.
    """

    block_id = validate_block_identifier(identifier)
    block_data = get_block(w3, block_id)
    print(to_json(block_data))


block_group.add_command(get)


@command()
@config_option
@rpc_endpoint_option
def height(w3: Web3) -> None:
    """Print the current block height for the chain."""

    print(w3.eth.block_number)


block_group.add_command(height)

"""
The "get" command group
"""

from autcli.utils import to_json, validate_block_identifier, web3_from_endpoint_arg
from autcli.options import rpc_endpoint_option
from autcli.user import get_block

from click import group, command, argument
from typing import Optional


@group(name="block")
def block_group() -> None:
    """
    Commands for querying block information.
    """


@command()
@rpc_endpoint_option
@argument("identifier", default="latest")
def get(rpc_endpoint: Optional[str], identifier: str) -> None:
    """
    Print information for block, where <identifier> is a block number or hash.
    """
    block_id = validate_block_identifier(identifier)
    w3 = web3_from_endpoint_arg(None, rpc_endpoint)
    block_data = get_block(w3, block_id)
    print(to_json(block_data))


block_group.add_command(get)

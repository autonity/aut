"""
The "get" command group
"""

from autcli.utils import to_json, validate_block_identifier, web3_from_endpoint_arg
from autcli.options import rpc_endpoint_option
from autcli.user import get_node_stats, get_block

from click import group, command, argument
from typing import Optional


@group()
def get() -> None:
    """
    Get blockchain information from the connected node.
    """


@command()
@rpc_endpoint_option
def stats(rpc_endpoint: Optional[str]) -> None:
    """
    Print general stats about RPC node and the blockchain it's on.
    """
    w3 = web3_from_endpoint_arg(None, rpc_endpoint)
    node_stats = get_node_stats(w3)
    print(to_json(node_stats, pretty=True))


@command()
@rpc_endpoint_option
@argument("identifier", default="latest")
def block(rpc_endpoint: Optional[str], identifier: str) -> None:
    """
    Print information for block, where <identifier> is a block number or hash.
    """
    block_id = validate_block_identifier(identifier)
    w3 = web3_from_endpoint_arg(None, rpc_endpoint)
    block_data = get_block(w3, block_id)
    print(to_json(block_data))


get.add_command(stats)
get.add_command(block)

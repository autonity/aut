"""
Implementation of `node` subcommands
"""

from aut.options import rpc_endpoint_option

from click import group, command
from typing import Optional, Union

# Disable pylint warning about imports outside top-level.  We do this
# intentionally to try and keep startup times of the CLI low.

# pylint: disable=import-outside-toplevel


@group(name="node")
def node_group() -> None:
    """
    Commands related to querying specific Autonity nodes.
    """


@command()
@rpc_endpoint_option
def info(rpc_endpoint: Optional[str]) -> None:
    """
    Print general information about the RPC node configuration and state.
    """
    from aut.utils import to_json, web3_from_endpoint_arg
    from web3.datastructures import AttributeDict
    from web3.types import SyncStatus

    w3 = web3_from_endpoint_arg(None, rpc_endpoint)
    admin_node_info = w3.geth.admin.node_info()

    # Handle eth_syncing as an AttributeDict or boolean
    syncing: Union[SyncStatus, bool] = w3.eth.syncing
    eth_syncing: Union[dict, bool] = (
        dict(syncing) if isinstance(syncing, AttributeDict) else False
    )
    node_info = {
        "eth_accounts": w3.eth.accounts,
        "eth_blockNumber": w3.eth.block_number,
        "eth_gasPrice": w3.eth.gas_price,
        "eth_hashrate": w3.eth.hashrate,
        "eth_mining": w3.eth.mining,
        "eth_syncing": eth_syncing,
        "eth_chainId": w3.eth.chain_id,
        "net_listening": w3.net.listening,
        "net_peerCount": w3.net.peer_count,
        "net_networkId": w3.net.version,
        "web3_clientVersion": w3.client_version,
        "admin_enode": admin_node_info["enode"],
        "admin_id": admin_node_info["id"],
    }

    print(to_json(node_info, pretty=True))


node_group.add_command(info)

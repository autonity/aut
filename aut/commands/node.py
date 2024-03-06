"""
Implementation of `node` subcommands
"""

from typing import Optional, Union

from click import command
from web3.datastructures import AttributeDict
from web3.types import SyncStatus

from aut.options import rpc_endpoint_option
from aut.utils import to_json, web3_from_endpoint_arg


@command()
@rpc_endpoint_option
def info(rpc_endpoint: Optional[str]) -> None:
    """
    Print general information about the RPC node configuration and state.
    """

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

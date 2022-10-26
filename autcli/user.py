"""
'User' functions. These functions encapsulate the functionality of
the CLI commands and emulate their usage as much as makes
sense. Return values are python types, as the 'commands' functions
hand json translation.

If aut implements an ipyothon 'console mode', perhaps these are the
functions meant to be called in that.
"""

from autcli.utils import w3_provider


from web3.types import (
    ChecksumAddress,
    Wei,
    BlockIdentifier,
    BlockData,
    TxReceipt,
    TxParams,
    SignedTx,
    HexBytes,
)
from typing import Dict, List, Tuple, Optional, Any


def get_account_stats(
    accounts: List[ChecksumAddress], tag: Optional[str] = None
) -> Dict[ChecksumAddress, Tuple[int, Wei]]:
    """
    For a list of accounts, return a dictionary with accounts as keys
    and list of transaction count and balance (in that order) as
    values. Tag is one of None, 'latest', 'earliest', 'pending' or a
    block number, and the values are as of block described by the
    tag. The underlying RPC methods are eth_getBalance and
    eth_getTransactionCount.
    """
    w3 = w3_provider()
    stats: Dict[ChecksumAddress, Tuple[int, Wei]] = {}
    for acct in accounts:
        txcount = w3.eth.get_transaction_count(acct)
        if tag is None:
            balance = w3.eth.get_balance(acct)
        else:
            balance = w3.eth.get_balance(acct, tag)
        stats[acct] = (txcount, balance)
    return stats


def get_node_stats() -> Any:
    """
    Return a dictionary with results for a bunch of of nullary EIP1474 RPC methods.
    """

    # TODO: types

    w3 = w3_provider()
    stats = {
        "eth_accounts": w3.eth.accounts,
        "eth_blockNumber": w3.eth.block_number,
        "eth_coinbase": w3.eth.coinbase,
        "eth_gasPrice": w3.eth.gas_price,
        "eth_hashrate": w3.eth.hashrate,
        "eth_mining": w3.eth.mining,
        "eth_syncing": w3.eth.syncing,
        "net_listening": w3.net.listening,
        "net_peerCount": w3.net.peer_count,
        "net_version": w3.net.version,
        "web3_clientVersion": w3.clientVersion,
    }
    return stats


def get_latest_block_number() -> int:
    """
    Returns the block height of the latest block.
    """
    w3 = w3_provider()
    block_number = w3.eth.block_number
    return block_number


def get_block(identifier: BlockIdentifier) -> BlockData:
    """
    Returns a dictionary of block data for the block identified by
    'identifier', which is either a block number/height or string
    representation of a 32 byte block hash.
    """
    w3 = w3_provider()
    block_data = w3.eth.get_block(identifier)
    return block_data


def get_transaction_receipt(tx_hash: HexBytes, wait_timeout: int = 0) -> TxReceipt:
    """
    Returns a dictionary with the tx receipt for the transaction
    identified by 'tx_hash'. If 'wait_timeout' is non-zero, wait that
    many seconds before returning a 'transactionNotFound' response,
    which is a useful feature as the tx hash is returned as soon as
    the RPC node gets the tx, but the receipt is not available until
    the tx has been mined.
    """
    w3 = w3_provider()
    if wait_timeout > 0:
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash, wait_timeout)
    else:
        tx_receipt = w3.eth.get_transaction_receipt(tx_hash)
    return tx_receipt


# TODO: support this?


def server_signtx(tx: TxParams) -> SignedTx:
    """
    Sign the transaction data contained in dictionary 'tx' by
    sending that data via web3 RPC call eth_signTransaction. The
    'from' account must be an account controlled by the RPC
    server/node.

    There are very few use-cases where this function should be called
    by an RPC client that does not reside on the same machine as the
    RPC server.
    """
    w3 = w3_provider()
    # TODO: this seems wrong somehow ...
    tx_raw = w3.eth.sign_transaction(tx["rawTransansaction"])  # type: ignore
    return tx_raw

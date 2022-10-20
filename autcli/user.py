"""
'User' functions. These functions encapsulate the functionality of
the CLI commands and emulate their usage as much as makes
sense. Return values are python types, as the 'commands' functions
hand json translation.

If aut implements an ipyothon 'console mode', perhaps these are the
functions meant to be called in that.
"""

from autcli.utils import address_keyfile_dict, w3_provider


def get_account_stats(accounts, tag=None):
    """
    For a list of accounts, return a dictionary with accounts as keys
    and list of transaction count and balance (in that order) as
    values. Tag is one of None, 'latest', 'earliest', 'pending' or a
    block number, and the values are as of block described by the
    tag. The underlying RPC methods are eth_getBalance and
    eth_getTransactionCount.
    """
    w3 = w3_provider()
    stats = {}
    for acct in accounts:
        txcount = w3.eth.get_transaction_count(acct)
        if tag is None:
            balance = w3.eth.get_balance(acct)
        else:
            balance = w3.eth.get_balance(acct, tag)
        stats[acct] = [txcount, balance]
    return stats


def get_account_transaction_count(account):
    """
    Return the transaction count of 'account'. Uses web3 method getTransactionCount.
    """
    w3 = w3_provider()
    transaction_count = w3.eth.get_transaction_count(account)
    return transaction_count


def get_node_stats():
    """
    Return a dictionary with results for a bunch of of nullary EIP1474 RPC methods.
    """
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


def get_latest_block_number():
    """
    Returns the block height of the latest block.
    """
    w3 = w3_provider()
    block_number = w3.eth.block_number
    return block_number


def get_block(identifier):
    """
    Returns a dictionary of block data for the block identified by
    'identifier', which is either a block number/height or string
    representation of a 32 byte block hash.
    """
    w3 = w3_provider()
    block_data = w3.eth.get_block(identifier)
    return block_data


def get_transaction_receipt(tx_hash, wait_timeout=0):
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


def client_signtx(tx, keystore_dir, keyfile_passphrase):
    """
    Sign the transaction data contained in dictionary 'tx' with a
    local keyfile in 'keystore_dir' and return raw signed tx
    bytes. Keyfiles are protected by a passphrase, so
    'keyfile_passphrase' is needed to decrypt the private_key
    contained in the file.
    """
    w3 = w3_provider()
    keyfiles = address_keyfile_dict(keystore_dir, degenerate_addr=True)
    keyfile_path = keyfiles[tx["from"].replace("0x", "").lower()]
    with open(keyfile_path, encoding="UTF-8") as keyfile:
        encrypted_key = keyfile.read()
        private_key = w3.eth.account.decrypt(encrypted_key, keyfile_passphrase)
    tx_raw = w3.eth.account.signTransaction(tx, private_key)
    return tx_raw


def server_signtx(tx):
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
    tx_raw = w3.eth.sign_transaction(tx)
    return tx_raw


def sendtx(tx_raw):
    """
    Send raw signed tx bytes provided by 'tx_raw' to an RPC server
    to be validated and included in the blockchain.
    """
    w3 = w3_provider()
    tx_hash = w3.eth.send_raw_transaction(tx_raw)
    return tx_hash

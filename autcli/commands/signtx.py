"""
Code that is executed when 'aut signtx..' is invoked on the command-line.
"""

from autcli.utils import load_from_file_or_stdin, to_json
from autcli.config import get_keyfile_password

from autonity.utils.tx import sign_tx

import sys
import json
from click import command, option, argument
from typing import Dict, Optional, Any, cast


@command()
@option("--key-file", "-k", required=True, help="Encrypted private key file")
@option("--password", "-p", help="Password for key file (or use env var 'KEYFILEPWD')")
@argument(
    "tx-file",
    required=True,
)
def signtx(key_file: str, password: Optional[str], tx_file: str) -> None:
    """
    Sign a transaction using the given keyfile.  Use '-' to read from
    stdin instead of a file.

    If password is not given, the env variable 'KEYFILEPWD' is used.
    If that is not set, the user is prompted.
    """

    # Read tx
    tx = json.loads(load_from_file_or_stdin(tx_file))

    # Read keyfile
    with open(key_file, encoding="ascii") as key_f:
        encrypted_key = json.load(key_f)

    # Read password
    password = get_keyfile_password(password)

    # Sign the tx:
    signed_tx = sign_tx(tx, encrypted_key, password)

    print(to_json(cast(Dict[Any, Any], signed_tx._asdict())))


# Other Features Contemplated
# ===========================
#
# Hardware Wallets
# ----------------
#
# extend client-signing usage like:
#
#  --trezor-sign    client-sign the transaction data using a trezor device.
#  --ledger-sign    client-sign the transaction data using a ledger device.
#
# trezor has a first-party python library, should be straightforward
# - https://pypi.org/project/trezor/
# - https://stackoverflow.com/questions/63608705/send-signed-transaction-from-trezor-hardware-wallet
#
# ledger looks like hard work via third-party solutions
# - https://pypi.org/project/ledgereth/ (BETA!)
# - https://gist.github.com/bargst/5f896e4a5984593d43f1b4eb66f79d68
# - https://github.com/ethereum/eth-account/issues/25
#
# but ledger recently open sourced their own, so maybe not too hard?
# - https://github.com/LedgerHQ/ledgerctl

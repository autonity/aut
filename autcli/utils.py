"""
Utility functions that are only meant to be called by other functions in this package.
"""

from autcli.config import get_rpc_endpoint
from autcli.constants import AutonDenoms

from autonity.utils.web3 import create_web3_for_endpoint
from autonity.utils.keyfile import load_keyfile

import os
import sys
from web3 import Web3
from web3.types import Wei, ChecksumAddress, BlockIdentifier
from typing import Dict, Optional, Any


def web3_from_endpoint_arg(w3: Optional[Web3], endpoint_arg: Optional[str]) -> Web3:
    """
    Construct a Web3 from a cli argument.  CLI argument is not
    present, fall back to env vars and config files.

    Used for the common pattern of initializing a Web3 on-demand, as
    required to compute parameter values not given on the command line
    For example, see the `maketx` command which may or may not connect
    to a node to compute one or more of: gas parameters, nonce,
    chainID, etc.  If multiple of these must be computed, we should
    avoid creating multiple connections.  Conversely, if all of these
    values are given on the command line, no connected web3 object is
    required.
    """
    if w3 is None:
        return create_web3_for_endpoint(get_rpc_endpoint(endpoint_arg))

    return w3


# TODO: remove
def w3_provider() -> Web3:
    """
    Return a web3py provider object for the RPC identifier that
    w3_provider_endpoint returns.
    """
    return Web3()  # web3_from_endpoint(w3_provider_endpoint())


def w3_provider_is_connected(w3: Web3) -> bool:
    """
    Take a web3py RPC provider object and return true if connected
    to the provider, otherwise throw exception.
    """
    # identifier = w3_provider_endpoint()
    if not w3.isConnected():
        raise OSError("Web3 is not connected")

    return True


def parse_wei_representation(wei_str: str) -> Wei:
    """
    Take a text representation of an integer with an optional
    denomination suffix (eg '2gwei' represents 2000000000
    wei). Returns an integer representing the value in wei.

    If no suffix is provided, just coerce the string into an
    integer. If integer coercion fails, throw an exception.
    """

    wei_str = wei_str.lower()
    try:
        if wei_str.endswith("kwei"):
            wei = int(wei_str[:-4]) * AutonDenoms.KWEI_VALUE_IN_WEI
        elif wei_str.endswith("mwei"):
            wei = int(wei_str[:-4]) * AutonDenoms.MWEI_VALUE_IN_WEI
        elif wei_str.endswith("gwei"):
            wei = int(wei_str[:-4]) * AutonDenoms.GWEI_VALUE_IN_WEI
        elif wei_str.endswith("szabo"):
            wei = int(wei_str[:-5]) * AutonDenoms.SZABO_VALUE_IN_WEI
        elif wei_str.endswith("finney"):
            wei = int(wei_str[:-6]) * AutonDenoms.FINNEY_VALUE_IN_WEI
        elif wei_str.endswith("auton"):
            wei = int(wei_str[:-5]) * AutonDenoms.AUTON_VALUE_IN_WEI
        elif wei_str.endswith("aut"):
            wei = int(wei_str[:-3]) * AutonDenoms.AUTON_VALUE_IN_WEI
        elif wei_str.endswith("wei"):
            wei = int(wei_str[:-3])
        else:
            wei = int(wei_str)
    except Exception as exc:
        raise Exception(
            f"{wei_str} is not a valid string representation of wei"
        ) from exc
    return Wei(wei)


def address_keyfile_dict(keystore_dir: str) -> Dict[ChecksumAddress, str]:
    """
    For directory 'keystore' that contains one or more keyfiles,
    return a dictionary with EIP55 checksum addresses as keys and
    keyfile path as value. If 'degenerate_addr', keys are addresses
    are all lower case and without the '0x' prefix.
    """
    addr_keyfile_dict: Dict[ChecksumAddress, str] = {}
    keyfile_list = os.listdir(keystore_dir)
    for fn in keyfile_list:
        keyfile_path = keystore_dir + "/" + fn
        keyfile = load_keyfile(keyfile_path)
        addr_lower = keyfile["address"]
        addr_keyfile_dict[Web3.toChecksumAddress("0x" + addr_lower)] = keyfile_path

    return addr_keyfile_dict


def degeneate_address_keyfile_dict(keystore_dir: str) -> Dict[str, str]:
    """
    Similar to address_keyfile_dict, but addresses (keys) are
    lower case and without the '0x' prefix.
    """
    addr_keyfile_dict = address_keyfile_dict(keystore_dir)
    return {k.lower().replace("0x", ""): v for k, v in addr_keyfile_dict.items()}


def to_checksum_address(address: str) -> ChecksumAddress:
    """
    Take a blockchain address as string, convert the string into
    an EIP55 checksum address and return that.
    """
    checksum_address = Web3.toChecksumAddress(address)
    return checksum_address


def to_json(data: Dict[Any, Any]) -> str:
    """
    Take python data structure, return json formatted data.
    """
    return Web3.toJSON(data)


def string_is_32byte_hash(hash_str: str) -> bool:
    """
    Test if string is valid, 0x-prefixed representation of a
    32-byte hash. If it is, return True, otherwise return False.
    """
    if not hash_str.startswith("0x"):
        return False
    if not len(hash_str) == 66:  # 66-2 = 64 hex digits = 32 bytes
        return False
    try:
        int(hash_str, 16)
        return True
    except Exception:  # pylint: disable=broad-except
        return False


def validate_32byte_hash_string(hash_str: str) -> str:
    """
    If string represents a valid 32-byte hash, just return it,
    otherwise raise exception.
    """
    if not string_is_32byte_hash(hash_str):
        raise Exception(f"{hash_str} is not a 32-byte hash")
    return hash_str


def validate_block_identifier(block_id: BlockIdentifier) -> BlockIdentifier:
    """
    If string represents a valid block identifier, just return it,
    otherwise raise exception. A valid block identifier is either a
    32-byte hash or a positive integer representing the block
    number. Note that 'validity' here does not mean that the block
    exists, we're just testing that the _format_ of x is valid.
    """

    if isinstance(block_id, int):
        return block_id

    if isinstance(block_id, str):
        if string_is_32byte_hash(block_id):
            return block_id

        # Attempt to parse as in int
        try:
            return int(block_id)
        except ValueError:
            pass

    raise ValueError(f"{str(block_id)} is neither a 32-byte hash nor an integer")


def load_from_file_or_stdin(filename: str) -> str:
    """
    Open a file and return the stream, where '-' represents stdin.
    """

    if filename == "-":
        return sys.stdin.read()

    with open(filename, "r", encoding="utf8") as in_f:
        return in_f.read()

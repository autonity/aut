"""
Utility functions that are only meant to be called by other functions in this package. 
"""
import os
import json
import re
from web3 import Web3
from autcli.constants import Defaults, AutonDenoms


def w3_provider_type(identifier):
    """
    Return the provider protocol type (https, ws, or IPC) of an
    endpoint described by string 'identifier'. If identifier isn't a
    valid format of one of these three types, return None.
    """
    regex_http = re.compile(r"^(?:http)s?://")
    regex_ws = re.compile(r"^(?:ws)s?://")
    regex_ipc = re.compile("([^ !$`&*()+]|(\\[ !$`&*()+]))+\\.ipc")
    if re.match(regex_http, identifier) is not None:
        return "http"
    if re.match(regex_ws, identifier) is not None:
        return "ws"
    if re.match(regex_ipc, identifier) is not None:
        return "ipc"
    return None


def validate_w3_provider_type(identifier):
    """
    Take identifier for an http or ws URI, or an IPC filepath and
    check that it's valid. If it's valid, just return identifier,
    otherwise raise exception.
    """
    rpc_type = w3_provider_type(identifier)
    if rpc_type is None:
        raise Exception(
            "rpc identifier must be an http|ws URI or a filesystem path to an IPC socket."
        )
    return identifier


def w3_provider_endpoint():
    """
    Return the identifier for the RPC provider endpoint. This will
    be the value of user's parent shell environment variable
    WEB3_PROVIDER, if that exists, otherwise the DEFAULT_RPC_ENDPOINT
    constant defined in this package.

    In the first case, the shell variable value is first validated and
    an exception thrown if it's not valid.
    """
    identifier = os.getenv("WEB3_PROVIDER")
    if identifier is not None:
        endpoint = validate_w3_provider_type(identifier)
    else:
        endpoint = Defaults.DEFAULT_RPC_ENDPOINT
    return endpoint


def w3_provider():
    """
    Return a web3py provider object for the RPC identifier that
    w3_provider_endpoint returns.
    """
    endpoint = w3_provider_endpoint()
    rpc_type = w3_provider_type(endpoint)
    if rpc_type == "http":
        return Web3(Web3.HTTPProvider(endpoint))
    if rpc_type == "ws":
        return Web3(Web3.WebsocketProvider(endpoint))
    if rpc_type == "ipc":
        return Web3(Web3.IPCProvider(endpoint))
    return None


def w3_provider_is_connected(w3):
    """
    Take a web3py RPC provider object and return true if connected
    to the provider, otherwise throw exception.
    """
    identifier = w3_provider_endpoint()
    if not w3.isConnected():
        raise Exception(
            f"{identifier} is not connected, "
            + "export WEB3_PROVIDER environment variable to a working provider."
        )
    return True


def parse_wei_representation(wei_str):
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
        else:
            wei = int(wei_str)
    except Exception as exc:
        raise Exception(
            f"{wei_str} is not a valid string representation of wei"
        ) from exc
    return wei


def address_keyfile_dict(keystore_dir, degenerate_addr=False):
    """
    For directory 'keystore' that contains one or more keyfiles,
    return a dictionary with EIP55 checksum addresses as keys and
    keyfile path as value. If 'degenerate_addr', keys are addresses
    are all lower case and without the '0x' prefix.
    """
    x = {}
    keyfile_list = os.listdir(keystore_dir)
    for fn in keyfile_list:
        keyfile_path = keystore_dir + "/" + fn
        keyfile = load_keyfile(keyfile_path)
        addr_lower = keyfile["address"]
        if degenerate_addr:
            x = {**x, **{addr_lower: keyfile_path}}
        else:
            addr_checksum = Web3.toChecksumAddress("0x" + addr_lower)
            x = {**x, **{addr_checksum: keyfile_path}}
    return x


def load_keyfile(keyfile_path):
    """
    Load a keyfile at keyfile_path and return its contents.
    """
    with open(keyfile_path, encoding="UTF-8") as keyfile:
        kf = keyfile.read()
    keyfile = json.loads(kf)
    return keyfile


def to_checksum_address(address):
    """
    Take a blockchain address as string, convert the string into
    an EIP55 checksum address and return that.
    """
    checksum_address = Web3.toChecksumAddress(address)
    return checksum_address


def to_json(data):
    """
    Take python data structure, return json formatted data.
    """
    json_data = Web3.toJSON(data)
    return json_data


def string_is_32byte_hash(x):
    """
    Test if string is valid, 0x-prefixed representation of a
    32-byte hash. If it is, return True, otherwise return False.
    """
    if not x.startswith("0x"):
        return False
    if not len(x) == 66:  # 66-2 = 64 hex digits = 32 bytes
        return False
    try:
        int(x, 16)
        return True
    except:
        return False


def validate_32byte_hash_string(x):
    """
    If string represents a valid 32-byte hash, just return it,
    otherwise raise exception.
    """
    if not string_is_32byte_hash(x):
        raise Exception(f"{x} is not a 32-byte hash")
    return x


def validate_block_identifier(x):
    """
    If string represents a valid block identifier, just return it,
    otherwise raise exception. A valid block identifier is either a
    32-byte hash or a positive integer representing the block
    number. Note that 'validity' here does not mean that the block
    exists, we're just testing that the _format_ of x is valid.
    """
    if string_is_32byte_hash(x):
        return x
    try:
        block_number = int(x)
        return block_number
    except ValueError as exc:
        raise Exception(f"{x} is neither a 32-byte hash nor an integer") from exc

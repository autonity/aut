from typing import Any

from autonity.utils.web3 import create_web3_for_endpoint
from click import ParamType
from eth_typing import ChecksumAddress
from hexbytes import HexBytes
from web3 import Web3
from web3.types import Wei


from .utils import parse_wei_representation


class RPCEndpointType(ParamType):
    name = "JSON-RPC endpoint"

    def convert(self, value: Any, *args) -> Web3:
        return create_web3_for_endpoint(value, ignore_chain_id=True)


class ChecksumAddressType(ParamType):
    name = "checksum address"

    def convert(self, value: Any, *args) -> ChecksumAddress:
        return Web3.to_checksum_address(value)


class HexBytesType(ParamType):
    name = "hex-bytes"

    def convert(self, value: Any, *args) -> HexBytes:
        return HexBytes(value)


class TokenValueType(ParamType):
    name = "token value"

    def convert(self, value: Any, *args) -> Wei:
        return parse_wei_representation(value)

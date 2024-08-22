from typing import Any

from eth_typing import ChecksumAddress
from web3 import Web3

from autonity.utils.web3 import create_web3_for_endpoint
from click import ParamType


class RPCEndpointType(ParamType):
    name = "JSON-RPC endpoint"

    def convert(self, value: Any, *args) -> Web3:
        return create_web3_for_endpoint(value, ignore_chain_id=True)


class ChecksumAddressType(ParamType):
    name = "checksum address"

    def convert(self, value: Any, *args) -> ChecksumAddress:
        return Web3.to_checksum_address(value)

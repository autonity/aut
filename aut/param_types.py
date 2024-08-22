from web3 import Web3
from typing import Any

from autonity.utils.web3 import create_web3_for_endpoint
from click import ParamType


class RPCEndpoint(ParamType):
    name = "JSON-RPC endpoint"

    def convert(self, value: Any, *args) -> Web3:
        return create_web3_for_endpoint(value, ignore_chain_id=True)

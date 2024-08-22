"""
The `contract` command group
"""

import json
from typing import List, Optional, Tuple, cast

from autonity.abi_parser import (
    find_abi_constructor,
    find_abi_function,
    parse_arguments,
    parse_return_value,
)
from click import ClickException, Path, argument, command, group, option
from web3 import Web3
from web3.contract.contract import ContractFunction

from ..logging import log
from ..options import (
    config_option,
    contract_options,
    from_option,
    keyfile_option,
    rpc_endpoint_option,
    tx_aux_options,
    tx_value_option,
)
from ..utils import (
    contract_address_and_abi_from_args,
    create_contract_tx_from_args,
    finalize_tx_from_args,
    from_address_from_argument,
    to_json,
)

# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
# pylint: disable=import-outside-toplevel


@group(name="contract")
def contract_group() -> None:
    """Command for interacting with arbitrary contracts."""


def function_call_from_args(
    w3: Web3,
    contract_address_str: str,
    contract_abi_path: str,
    method: str,
    parameters: List[str],
) -> Tuple:
    """Construct a ContractFunction object.

    Take command line arguments and construct a ContractFunction
    (i.e. a function call). Returns the ContractFunction object, the
    ABIFunction for the method, and the Web3 object created in the
    process.
    """

    log(f"method: {method}")
    log(f"parameters: {list(parameters)}")

    address, abi = contract_address_and_abi_from_args(
        contract_address_str, contract_abi_path
    )

    abi_fn = find_abi_function(abi, method)
    fn_params = parse_arguments(abi_fn, parameters)
    log(f"fn_params (parsed): {fn_params}")

    contract = w3.eth.contract(address, abi=abi)
    contract_fn = getattr(contract.functions, method, None)
    if contract_fn is None:
        raise ClickException(f"method '{method}' not found on contract abi")

    return contract_fn(*fn_params), abi_fn


@command(name="deploy")
@config_option
@rpc_endpoint_option
@keyfile_option()
@from_option
@tx_value_option()
@tx_aux_options
@option(
    "--contract",
    "contract_path",
    required=True,
    type=Path(),
    help="Path to JSON file holding contact abi and bytecode.",
)
@argument("parameters", nargs=-1)
def deploy_cmd(
    w3: Web3,
    keyfile: Optional[str],
    from_str: Optional[str],
    contract_path: str,
    gas: Optional[str],
    gas_price: Optional[str],
    max_priority_fee_per_gas: Optional[str],
    max_fee_per_gas: Optional[str],
    fee_factor: Optional[float],
    nonce: Optional[int],
    value: Optional[str],
    chain_id: Optional[int],
    parameters: List[str],
) -> None:
    """Deploy a contract, given the compiled JSON file.

    Note that the contract's address will appear in the 'contractAddress' field of
    the transaction receipt (see `aut tx wait`).
    """

    log(f"parameters: {list(parameters)}")

    # load contract
    with open(contract_path, "r", encoding="utf8") as contract_f:
        compiled = json.load(contract_f)

    contract = w3.eth.contract(abi=compiled["abi"], bytecode=compiled["bytecode"])

    abi_fn = find_abi_constructor(contract.abi)
    fn_params = parse_arguments(abi_fn, parameters)
    log(f"fn_params (parsed): {fn_params}")
    deploy_fn = cast(ContractFunction, contract.constructor(*fn_params))

    from_addr = from_address_from_argument(from_str, keyfile)

    deploy_tx = create_contract_tx_from_args(
        function=deploy_fn,
        from_addr=from_addr,
        value=value,
        gas=gas,
        gas_price=gas_price,
        max_fee_per_gas=max_fee_per_gas,
        max_priority_fee_per_gas=max_priority_fee_per_gas,
        fee_factor=fee_factor,
        nonce=nonce,
        chain_id=chain_id,
    )

    del deploy_tx["to"]

    tx = finalize_tx_from_args(w3, deploy_tx, from_addr)
    print(to_json(tx))


contract_group.add_command(deploy_cmd)


@command(name="call")
@config_option
@rpc_endpoint_option
@contract_options
@argument("method")
@argument("parameters", nargs=-1)
def call_cmd(
    w3: Web3,
    contract_address_str: str,
    contract_abi_path: str,
    method: str,
    parameters: List[str],
) -> None:
    """Execute a contract call on the connected node, and print the result."""

    function, abi_fn = function_call_from_args(
        w3,
        contract_address_str,
        contract_abi_path,
        method,
        parameters,
    )

    result = function.call()
    parsed_result = parse_return_value(abi_fn, result)
    print(to_json(parsed_result))


contract_group.add_command(call_cmd)


@command(name="tx")
@config_option
@rpc_endpoint_option
@keyfile_option()
@from_option
@contract_options
@tx_value_option()
@tx_aux_options
@argument("method")
@argument("parameters", nargs=-1)
def tx_cmd(
    w3: Web3,
    keyfile: Optional[str],
    from_str: Optional[str],
    contract_address_str: str,
    contract_abi_path: str,
    method: str,
    parameters: List[str],
    gas: Optional[str],
    gas_price: Optional[str],
    max_priority_fee_per_gas: Optional[str],
    max_fee_per_gas: Optional[str],
    fee_factor: Optional[float],
    nonce: Optional[int],
    value: Optional[str],
    chain_id: Optional[int],
) -> None:
    """Create a transaction which calls the given contract method, passing any
    parameters.

    The parameters must match those required by the contract.
    """

    function, _ = function_call_from_args(
        w3,
        contract_address_str,
        contract_abi_path,
        method,
        parameters,
    )

    from_addr = from_address_from_argument(from_str, keyfile)
    log(f"from_addr: {from_addr}")

    tx = create_contract_tx_from_args(
        function=function,
        from_addr=from_addr,
        value=value,
        gas=gas,
        gas_price=gas_price,
        max_fee_per_gas=max_fee_per_gas,
        max_priority_fee_per_gas=max_priority_fee_per_gas,
        fee_factor=fee_factor,
        nonce=nonce,
        chain_id=chain_id,
    )

    # Fill in any missing values.

    tx = finalize_tx_from_args(w3, tx, from_addr)
    print(to_json(tx))


contract_group.add_command(tx_cmd)

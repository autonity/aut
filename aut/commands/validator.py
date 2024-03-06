"""
The `validator` command group.
"""

import sys
from typing import Optional
from urllib import parse as urlparse

from autonity.autonity import Autonity
from autonity.utils.denominations import format_auton_quantity
from autonity.validator import OracleAddress, Validator
from click import argument, command, echo, option
from web3 import Web3
from web3.types import HexBytes

from aut.config import get_node_address
from aut.constants import UnixExitStatus
from aut.options import (from_option, keyfile_option, rpc_endpoint_option,
                         tx_aux_options, validator_option)
from aut.utils import (autonity_from_endpoint_arg,
                       create_contract_tx_from_args,
                       from_address_from_argument, parse_commission_rate,
                       parse_newton_value_representation, to_json,
                       web3_from_endpoint_arg)

# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals

# TODO: consider caching the LNTN addresses of Validators


@command()
@rpc_endpoint_option
@validator_option
def info(rpc_endpoint: Optional[str], validator_addr_str: str) -> None:
    """
    Get information about a validator.
    """

    validator_addr = get_node_address(validator_addr_str)
    aut = autonity_from_endpoint_arg(rpc_endpoint)
    validator_data = aut.get_validator(validator_addr)
    if (
        validator_data is None
        or validator_data.get("node_address", "") != validator_addr
    ):
        echo(
            f"The address {validator_addr} is not registered as a validator.",
            err=True,
        )
        sys.exit(UnixExitStatus.WEB3_RESOURCE_NOT_FOUND)
    echo(to_json(aut.get_validator(validator_addr), pretty=True))


@command()
@argument("enode")
def compute_address(
    enode: str,
) -> None:
    """
    Compute the address corresponding to an enode URL.
    """

    _, key_at_ip_port, _, _, _, _ = urlparse.urlparse(enode)
    pubkey, _ = key_at_ip_port.split("@")
    addr_bytes = Web3.keccak(bytes(HexBytes(pubkey)))[-20:]
    print(Web3.to_checksum_address(addr_bytes.hex()))


@command()
@rpc_endpoint_option
@keyfile_option()
@from_option
@tx_aux_options
@validator_option
@argument("amount-str", metavar="AMOUNT", nargs=1)
def bond(
    rpc_endpoint: Optional[str],
    keyfile: Optional[str],
    from_str: Optional[str],
    gas: Optional[str],
    gas_price: Optional[str],
    max_priority_fee_per_gas: Optional[str],
    max_fee_per_gas: Optional[str],
    fee_factor: Optional[float],
    nonce: Optional[int],
    chain_id: Optional[int],
    validator_addr_str: Optional[str],
    amount_str: str,
) -> None:
    """
    Create transaction to bond Newton to a validator.
    """

    token_units = parse_newton_value_representation(amount_str)
    validator_addr = get_node_address(validator_addr_str)
    from_addr = from_address_from_argument(from_str, keyfile)

    aut = autonity_from_endpoint_arg(rpc_endpoint)

    tx = create_contract_tx_from_args(
        function=aut.bond(validator_addr, token_units),
        from_addr=from_addr,
        gas=gas,
        gas_price=gas_price,
        max_fee_per_gas=max_fee_per_gas,
        max_priority_fee_per_gas=max_priority_fee_per_gas,
        fee_factor=fee_factor,
        nonce=nonce,
        chain_id=chain_id,
    )
    print(to_json(tx))


@command()
@rpc_endpoint_option
@keyfile_option()
@from_option
@tx_aux_options
@validator_option
@argument("amount-str", metavar="AMOUNT", nargs=1)
def unbond(
    rpc_endpoint: Optional[str],
    keyfile: Optional[str],
    from_str: Optional[str],
    gas: Optional[str],
    gas_price: Optional[str],
    max_priority_fee_per_gas: Optional[str],
    max_fee_per_gas: Optional[str],
    fee_factor: Optional[float],
    nonce: Optional[int],
    chain_id: Optional[int],
    validator_addr_str: Optional[str],
    amount_str: str,
) -> None:
    """
    Create transaction to unbond Newton from a validator.
    """

    token_units = parse_newton_value_representation(amount_str)
    validator_addr = get_node_address(validator_addr_str)
    from_addr = from_address_from_argument(from_str, keyfile)

    aut = autonity_from_endpoint_arg(rpc_endpoint)

    tx = create_contract_tx_from_args(
        function=aut.unbond(validator_addr, token_units),
        from_addr=from_addr,
        gas=gas,
        gas_price=gas_price,
        max_fee_per_gas=max_fee_per_gas,
        max_priority_fee_per_gas=max_priority_fee_per_gas,
        fee_factor=fee_factor,
        nonce=nonce,
        chain_id=chain_id,
    )
    print(to_json(tx))


@command()
@rpc_endpoint_option
@keyfile_option()
@from_option
@tx_aux_options
@argument("enode")
@argument("oracle")
@argument("consensus_key")
@argument("proof")
def register(
    rpc_endpoint: Optional[str],
    keyfile: Optional[str],
    from_str: Optional[str],
    gas: Optional[str],
    gas_price: Optional[str],
    max_priority_fee_per_gas: Optional[str],
    max_fee_per_gas: Optional[str],
    fee_factor: Optional[float],
    nonce: Optional[int],
    chain_id: Optional[int],
    enode: str,
    oracle: OracleAddress,
    consensus_key: str,
    proof: str,
) -> None:
    """
    Create transaction to register a validator
    """

    consensus_key_bytes = HexBytes(consensus_key)
    proof_bytes = HexBytes(proof)

    from_addr = from_address_from_argument(from_str, keyfile)
    # TODO: validate enode string?

    aut = autonity_from_endpoint_arg(rpc_endpoint)
    tx = create_contract_tx_from_args(
        function=aut.register_validator(
            enode, oracle, consensus_key_bytes, proof_bytes
        ),
        from_addr=from_addr,
        gas=gas,
        gas_price=gas_price,
        max_fee_per_gas=max_fee_per_gas,
        max_priority_fee_per_gas=max_priority_fee_per_gas,
        fee_factor=fee_factor,
        nonce=nonce,
        chain_id=chain_id,
    )
    print(to_json(tx))


@command()
@rpc_endpoint_option
@keyfile_option()
@from_option
@tx_aux_options
@validator_option
def pause(
    rpc_endpoint: Optional[str],
    keyfile: Optional[str],
    from_str: Optional[str],
    gas: Optional[str],
    gas_price: Optional[str],
    max_priority_fee_per_gas: Optional[str],
    max_fee_per_gas: Optional[str],
    fee_factor: Optional[float],
    nonce: Optional[int],
    chain_id: Optional[int],
    validator_addr_str: Optional[str],
) -> None:
    """
    Create transaction to pause the given validator.  See
    `pauseValidator` on the Autonity contract.
    """

    validator_addr = get_node_address(validator_addr_str)
    from_addr = from_address_from_argument(from_str, keyfile)

    aut = autonity_from_endpoint_arg(rpc_endpoint)

    tx = create_contract_tx_from_args(
        function=aut.pause_validator(validator_addr),
        from_addr=from_addr,
        gas=gas,
        gas_price=gas_price,
        max_fee_per_gas=max_fee_per_gas,
        max_priority_fee_per_gas=max_priority_fee_per_gas,
        fee_factor=fee_factor,
        nonce=nonce,
        chain_id=chain_id,
    )
    print(to_json(tx))


@command()
@rpc_endpoint_option
@keyfile_option()
@from_option
@tx_aux_options
@validator_option
def activate(
    rpc_endpoint: Optional[str],
    keyfile: Optional[str],
    from_str: Optional[str],
    gas: Optional[str],
    gas_price: Optional[str],
    max_priority_fee_per_gas: Optional[str],
    max_fee_per_gas: Optional[str],
    fee_factor: Optional[float],
    nonce: Optional[int],
    chain_id: Optional[int],
    validator_addr_str: Optional[str],
) -> None:
    """
    Create transaction to activate a paused validator.  See
    `activateValidator` on the Autonity contract.
    """

    validator_addr = get_node_address(validator_addr_str)
    from_addr = from_address_from_argument(from_str, keyfile)

    aut = autonity_from_endpoint_arg(rpc_endpoint)

    tx = create_contract_tx_from_args(
        function=aut.activate_validator(validator_addr),
        from_addr=from_addr,
        gas=gas,
        gas_price=gas_price,
        max_fee_per_gas=max_fee_per_gas,
        max_priority_fee_per_gas=max_priority_fee_per_gas,
        fee_factor=fee_factor,
        nonce=nonce,
        chain_id=chain_id,
    )
    print(to_json(tx))


@command()
@rpc_endpoint_option
@keyfile_option()
@from_option
@tx_aux_options
@validator_option
@argument("rate", type=str, nargs=1)
def change_commission_rate(
    rpc_endpoint: Optional[str],
    keyfile: Optional[str],
    from_str: Optional[str],
    gas: Optional[str],
    gas_price: Optional[str],
    max_priority_fee_per_gas: Optional[str],
    max_fee_per_gas: Optional[str],
    fee_factor: Optional[float],
    nonce: Optional[int],
    chain_id: Optional[int],
    validator_addr_str: Optional[str],
    rate: str,
) -> None:
    """
    Create transaction to change the commission rate for the given
    Validator.  The rate is given as a decimal, and must be no greater
    than 1 e.g. 3% would be 0.03.
    """

    validator_addr = get_node_address(validator_addr_str)
    from_addr = from_address_from_argument(from_str, keyfile)

    aut = autonity_from_endpoint_arg(rpc_endpoint)

    rate_precision = aut.commission_rate_precision()
    rate_int = parse_commission_rate(rate, rate_precision)

    tx = create_contract_tx_from_args(
        function=aut.change_commission_rate(validator_addr, rate_int),
        from_addr=from_addr,
        gas=gas,
        gas_price=gas_price,
        max_fee_per_gas=max_fee_per_gas,
        max_priority_fee_per_gas=max_priority_fee_per_gas,
        fee_factor=fee_factor,
        nonce=nonce,
        chain_id=chain_id,
    )
    print(to_json(tx))


@command()
@rpc_endpoint_option
@keyfile_option()
@validator_option
@option("--account", help="Delegator account to check")
def unclaimed_rewards(
    rpc_endpoint: Optional[str],
    keyfile: Optional[str],
    validator_addr_str: Optional[str],
    account: Optional[str],
) -> None:
    """
    Check the given validator for unclaimed-fees.
    """

    validator_addr = get_node_address(validator_addr_str)
    account = from_address_from_argument(account, keyfile)

    aut = autonity_from_endpoint_arg(rpc_endpoint)
    vdesc = aut.get_validator(validator_addr)
    val = Validator(aut.contract.w3, vdesc)
    unclaimed_wei = val.unclaimed_rewards(account)
    print(format_auton_quantity(unclaimed_wei))


@command()
@rpc_endpoint_option
@keyfile_option()
@from_option
@tx_aux_options
@validator_option
def claim_rewards(
    rpc_endpoint: Optional[str],
    keyfile: Optional[str],
    from_str: Optional[str],
    gas: Optional[str],
    gas_price: Optional[str],
    max_priority_fee_per_gas: Optional[str],
    max_fee_per_gas: Optional[str],
    fee_factor: Optional[float],
    nonce: Optional[int],
    chain_id: Optional[int],
    validator_addr_str: Optional[str],
) -> None:
    """
    Create transaction to claim rewards from a Validator.
    """

    validator_addr = get_node_address(validator_addr_str)
    from_addr = from_address_from_argument(from_str, keyfile)

    w3 = web3_from_endpoint_arg(None, rpc_endpoint)
    aut = Autonity(w3)
    vdesc = aut.get_validator(validator_addr)
    val = Validator(w3, vdesc)

    tx = create_contract_tx_from_args(
        function=val.claim_rewards(),
        from_addr=from_addr,
        gas=gas,
        gas_price=gas_price,
        max_fee_per_gas=max_fee_per_gas,
        max_priority_fee_per_gas=max_priority_fee_per_gas,
        fee_factor=fee_factor,
        nonce=nonce,
        chain_id=chain_id,
    )
    print(to_json(tx))

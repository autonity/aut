"""
The `validator` command group.
"""

import sys
from typing import Optional
from urllib import parse as urlparse

from autonity.autonity import Autonity
from autonity.utils.denominations import format_auton_quantity, format_newton_quantity
from autonity.validator import NodeAddress, OracleAddress, Validator
from click import argument, command, echo, group, option
from eth_typing import ChecksumAddress
from hexbytes import HexBytes
from web3 import Web3

from ..commands.protocol import protocol_group
from ..constants import UnixExitStatus
from ..options import (
    config_option,
    from_option,
    keyfile_option,
    rpc_endpoint_option,
    tx_aux_options,
    validator_option,
)
from ..param_types import ChecksumAddressType
from ..utils import (
    create_contract_tx_from_args,
    from_address_from_argument,
    parse_commission_rate,
    parse_newton_value_representation,
    to_json,
)

# Disable pylint warning about imports outside top-level.  We do this
# intentionally to try and keep startup times of the CLI low.

# pylint: disable=import-outside-toplevel
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals

# TODO: consider caching the LNTN addresses of Validators


@group()
def validator() -> None:
    """Commands related to the validators."""


validator.add_command(
    protocol_group.get_command(None, "validators"),  # type: ignore
    name="list",
)


@command()
@config_option
@rpc_endpoint_option
@validator_option
def info(w3: Web3, validator_addr: NodeAddress) -> None:
    """Get information about a validator."""

    aut = Autonity(w3)
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


validator.add_command(info)


@command()
@config_option
@argument("enode")
def compute_address(
    enode: str,
) -> None:
    """Compute the address corresponding to an enode URL."""

    _, key_at_ip_port, _, _, _, _ = urlparse.urlparse(enode)
    pubkey, _ = key_at_ip_port.split("@")
    addr_bytes = Web3.keccak(bytes(HexBytes(pubkey)))[-20:]
    print(Web3.to_checksum_address(addr_bytes.hex()))


validator.add_command(compute_address)


@command()
@config_option
@rpc_endpoint_option
@keyfile_option()
@from_option
@tx_aux_options
@validator_option
@argument("amount-str", metavar="AMOUNT", nargs=1)
def bond(
    w3: Web3,
    keyfile: Optional[str],
    from_: Optional[ChecksumAddress],
    gas: Optional[str],
    gas_price: Optional[str],
    max_priority_fee_per_gas: Optional[str],
    max_fee_per_gas: Optional[str],
    fee_factor: Optional[float],
    nonce: Optional[int],
    chain_id: Optional[int],
    validator: NodeAddress,
    amount_str: str,
) -> None:
    """Create transaction to bond Newton to a validator."""

    token_units = parse_newton_value_representation(amount_str)
    from_addr = from_address_from_argument(from_, keyfile)

    aut = Autonity(w3)

    tx = create_contract_tx_from_args(
        function=aut.bond(validator, token_units),
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


validator.add_command(bond)


@command()
@config_option
@rpc_endpoint_option
@keyfile_option()
@from_option
@tx_aux_options
@validator_option
@argument("amount-str", metavar="AMOUNT", nargs=1)
def unbond(
    w3: Web3,
    keyfile: Optional[str],
    from_: Optional[ChecksumAddress],
    gas: Optional[str],
    gas_price: Optional[str],
    max_priority_fee_per_gas: Optional[str],
    max_fee_per_gas: Optional[str],
    fee_factor: Optional[float],
    nonce: Optional[int],
    chain_id: Optional[int],
    validator: NodeAddress,
    amount_str: str,
) -> None:
    """Create transaction to unbond Newton from a validator."""

    token_units = parse_newton_value_representation(amount_str)
    from_addr = from_address_from_argument(from_, keyfile)

    aut = Autonity(w3)

    tx = create_contract_tx_from_args(
        function=aut.unbond(validator, token_units),
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


validator.add_command(unbond)


@command()
@config_option
@rpc_endpoint_option
@keyfile_option()
@from_option
@tx_aux_options
@argument("enode")
@argument("oracle", type=ChecksumAddressType())
@argument("consensus_key")
@argument("proof")
def register(
    w3: Web3,
    keyfile: Optional[str],
    from_: Optional[ChecksumAddress],
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
    """Create transaction to register a validator."""

    consensus_key_bytes = HexBytes(consensus_key)
    proof_bytes = HexBytes(proof)

    from_addr = from_address_from_argument(from_, keyfile)
    # TODO: validate enode string?

    aut = Autonity(w3)
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


validator.add_command(register)


@command()
@config_option
@rpc_endpoint_option
@keyfile_option()
@from_option
@tx_aux_options
@validator_option
def pause(
    w3: Web3,
    keyfile: Optional[str],
    from_: Optional[ChecksumAddress],
    gas: Optional[str],
    gas_price: Optional[str],
    max_priority_fee_per_gas: Optional[str],
    max_fee_per_gas: Optional[str],
    fee_factor: Optional[float],
    nonce: Optional[int],
    chain_id: Optional[int],
    validator: NodeAddress,
) -> None:
    """Create transaction to pause the given validator.

    See `pauseValidator` on the Autonity contract.
    """

    from_addr = from_address_from_argument(from_, keyfile)

    aut = Autonity(w3)

    tx = create_contract_tx_from_args(
        function=aut.pause_validator(validator),
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


validator.add_command(pause)


@command()
@config_option
@rpc_endpoint_option
@keyfile_option()
@from_option
@tx_aux_options
@validator_option
def activate(
    w3: Web3,
    keyfile: Optional[str],
    from_: Optional[ChecksumAddress],
    gas: Optional[str],
    gas_price: Optional[str],
    max_priority_fee_per_gas: Optional[str],
    max_fee_per_gas: Optional[str],
    fee_factor: Optional[float],
    nonce: Optional[int],
    chain_id: Optional[int],
    validator: NodeAddress,
) -> None:
    """Create transaction to activate a paused validator.

    See `activateValidator` on the Autonity contract.
    """

    from_addr = from_address_from_argument(from_, keyfile)

    aut = Autonity(w3)

    tx = create_contract_tx_from_args(
        function=aut.activate_validator(validator),
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


validator.add_command(activate)


@command()
@config_option
@rpc_endpoint_option
@keyfile_option()
@from_option
@tx_aux_options
@validator_option
@argument("rate", type=str, nargs=1)
def change_commission_rate(
    w3: Web3,
    keyfile: Optional[str],
    from_: Optional[ChecksumAddress],
    gas: Optional[str],
    gas_price: Optional[str],
    max_priority_fee_per_gas: Optional[str],
    max_fee_per_gas: Optional[str],
    fee_factor: Optional[float],
    nonce: Optional[int],
    chain_id: Optional[int],
    validator: NodeAddress,
    rate: str,
) -> None:
    """Create transaction to change the commission rate for the given Validator.

    The rate is given as a decimal, and must be no greater than 1 e.g. 3% would be 0.03.
    """

    from_addr = from_address_from_argument(from_, keyfile)

    aut = Autonity(w3)

    rate_precision = aut.commission_rate_precision()
    rate_int = parse_commission_rate(rate, rate_precision)

    tx = create_contract_tx_from_args(
        function=aut.change_commission_rate(validator, rate_int),
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


validator.add_command(change_commission_rate)


@command()
@config_option
@rpc_endpoint_option
@keyfile_option()
@validator_option
@option("--ntn", is_flag=True, help="Check Newton (NTN) instead of Auton")
@option("--account", type=ChecksumAddressType(), help="Delegator account to check")
def unclaimed_rewards(
    w3: Web3,
    keyfile: Optional[str],
    ntn: bool,
    validator: NodeAddress,
    account: Optional[ChecksumAddress],
) -> None:
    """Check the given validator for unclaimed fees."""

    account = from_address_from_argument(account, keyfile)

    aut = Autonity(w3)
    vdesc = aut.get_validator(validator)
    val = Validator(aut.contract.w3, vdesc)
    unclaimed_atn, unclaimed_ntn = val.unclaimed_rewards(account)
    print(
        format_newton_quantity(unclaimed_ntn)
        if ntn
        else format_auton_quantity(unclaimed_atn)
    )


validator.add_command(unclaimed_rewards)


@command()
@config_option
@rpc_endpoint_option
@keyfile_option()
@from_option
@tx_aux_options
@validator_option
def claim_rewards(
    w3: Web3,
    keyfile: Optional[str],
    from_: Optional[ChecksumAddress],
    gas: Optional[str],
    gas_price: Optional[str],
    max_priority_fee_per_gas: Optional[str],
    max_fee_per_gas: Optional[str],
    fee_factor: Optional[float],
    nonce: Optional[int],
    chain_id: Optional[int],
    validator: NodeAddress,
) -> None:
    """Create transaction to claim rewards from a Validator."""

    from_addr = from_address_from_argument(from_, keyfile)

    aut = Autonity(w3)
    vdesc = aut.get_validator(validator)
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


validator.add_command(claim_rewards)


@command()
@config_option
@rpc_endpoint_option
@keyfile_option()
@from_option
@tx_aux_options
@validator_option
@argument("enode", nargs=1)
def update_enode(
    w3: Web3,
    keyfile: Optional[str],
    from_: Optional[ChecksumAddress],
    gas: Optional[str],
    gas_price: Optional[str],
    max_priority_fee_per_gas: Optional[str],
    max_fee_per_gas: Optional[str],
    fee_factor: Optional[float],
    nonce: Optional[int],
    chain_id: Optional[int],
    validator: NodeAddress,
    enode: str,
) -> None:
    """Update the enode of a registered validator.

    This function updates the network connection information (IP or/and port)
    of a registered validator. You cannot change the validator's address
    (pubkey part of the enode).
    """

    from_addr = from_address_from_argument(from_, keyfile)

    aut = Autonity(w3)

    tx = create_contract_tx_from_args(
        function=aut.update_enode(validator, enode),
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


validator.add_command(update_enode)

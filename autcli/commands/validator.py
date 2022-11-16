"""
The `validator` command group.
"""

from autcli.config import get_validator_address
from autcli.options import (
    rpc_endpoint_option,
    keyfile_option,
    from_option,
    tx_aux_options,
    validator_option,
)
from autcli.utils import (
    web3_from_endpoint_arg,
    from_address_from_argument,
    to_json,
    create_contract_tx_from_args,
    parse_wei_representation,
)
from autcli.commands.autonity import autonity as autonity_cmd

from autonity.autonity import Autonity
from autonity.validator import Validator

from click import group, command, option, argument

from typing import Optional

# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals

# TODO: consider caching the LNEW addresses of Validators


@group()
def validator() -> None:
    """
    Commands related to the validators.
    """


validator.add_command(autonity_cmd.get_command(None, "get-validators"), name="list")  # type: ignore


@command()
@rpc_endpoint_option
@validator_option
def info(rpc_endpoint: Optional[str], validator_addr_str: str) -> None:
    """
    Get information about a validator.
    """
    validator_addr = get_validator_address(validator_addr_str)
    aut = Autonity(web3_from_endpoint_arg(None, rpc_endpoint))
    print(to_json(aut.get_validator(validator_addr), pretty=True))


validator.add_command(info)


@command()
@rpc_endpoint_option
@keyfile_option()
@from_option
@tx_aux_options
@validator_option
@argument("amount-str", metavar="AMOUNT", nargs=1)
def bond(
    rpc_endpoint: Optional[str],
    key_file: Optional[str],
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
    amount = parse_wei_representation(amount_str)
    validator_addr = get_validator_address(validator_addr_str)
    from_addr = from_address_from_argument(from_str, key_file)

    w3 = web3_from_endpoint_arg(None, rpc_endpoint)
    aut = Autonity(w3)

    tx = create_contract_tx_from_args(
        function=aut.bond(validator_addr, amount),
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
@rpc_endpoint_option
@keyfile_option()
@from_option
@tx_aux_options
@validator_option
@argument("amount-str", metavar="AMOUNT", nargs=1)
def unbond(
    rpc_endpoint: Optional[str],
    key_file: Optional[str],
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
    amount = parse_wei_representation(amount_str)
    validator_addr = get_validator_address(validator_addr_str)
    from_addr = from_address_from_argument(from_str, key_file)

    w3 = web3_from_endpoint_arg(None, rpc_endpoint)
    aut = Autonity(w3)

    tx = create_contract_tx_from_args(
        function=aut.unbond(validator_addr, amount),
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
@rpc_endpoint_option
@keyfile_option()
@from_option
@tx_aux_options
@argument("enode")
def register(
    rpc_endpoint: Optional[str],
    key_file: Optional[str],
    from_str: Optional[str],
    gas: Optional[str],
    gas_price: Optional[str],
    max_priority_fee_per_gas: Optional[str],
    max_fee_per_gas: Optional[str],
    fee_factor: Optional[float],
    nonce: Optional[int],
    chain_id: Optional[int],
    enode: str,
) -> None:
    """
    Create transaction to register a validator
    """
    from_addr = from_address_from_argument(from_str, key_file)
    # TODO: validate enode string?

    w3 = web3_from_endpoint_arg(None, rpc_endpoint)
    aut = Autonity(w3)
    tx = create_contract_tx_from_args(
        function=aut.register_validator(enode),
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
@rpc_endpoint_option
@keyfile_option()
@from_option
@tx_aux_options
@validator_option
def pause(
    rpc_endpoint: Optional[str],
    key_file: Optional[str],
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
    validator_addr = get_validator_address(validator_addr_str)
    from_addr = from_address_from_argument(from_str, key_file)

    w3 = web3_from_endpoint_arg(None, rpc_endpoint)
    aut = Autonity(w3)

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


validator.add_command(pause)


@command()
@rpc_endpoint_option
@keyfile_option()
@from_option
@tx_aux_options
@validator_option
def activate(
    rpc_endpoint: Optional[str],
    key_file: Optional[str],
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
    validator_addr = get_validator_address(validator_addr_str)
    from_addr = from_address_from_argument(from_str, key_file)

    w3 = web3_from_endpoint_arg(None, rpc_endpoint)
    aut = Autonity(w3)

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


validator.add_command(activate)


# TODO: enable this once the call is available.

# @command()
# @rpc_endpoint_option
# @keyfile_option()
# @from_option
# @tx_aux_options
# @validator_option
# @argument("rate", type=float, nargs=1)
# def change_commission_rate(
#     rpc_endpoint: Optional[str],
#     key_file: Optional[str],
#     from_str: Optional[str],
#     gas: Optional[str],
#     gas_price: Optional[str],
#     max_priority_fee_per_gas: Optional[str],
#     max_fee_per_gas: Optional[str],
#     fee_factor: Optional[float],
#     nonce: Optional[int],
#     chain_id: Optional[int],
#     validator_addr_str: Optional[str],
#     rate: float,
# ) -> None:
#     """
#     Create transaction to set the commission rate for the given
#     Validator.  See `changeCommissionRate` on the Autonity contract.
#     """
#     validator_addr = get_validator_address(validator_addr_str)
#     from_addr = from_address_from_argument(from_str, key_file)

#     w3 = web3_from_endpoint_arg(None, rpc_endpoint)
#     aut = Autonity(w3)

#     rate_precision = aut.commission_rate_precision()
#     rate_int = int(rate * rate_precision)

#     tx = create_contract_tx_from_args(
#         function=aut.change_commission_rate(validator_addr, rate_int),
#         from_addr=from_addr,
#         gas=gas,
#         gas_price=gas_price,
#         max_fee_per_gas=max_fee_per_gas,
#         max_priority_fee_per_gas=max_priority_fee_per_gas,
#         fee_factor=fee_factor,
#         nonce=nonce,
#         chain_id=chain_id,
#     )
#     print(to_json(tx))


# validator.add_command(change_commission_rate)


@command()
@rpc_endpoint_option
@keyfile_option()
@validator_option
@option("--account", help="Delegator account to check")
def unclaimed_rewards(
    rpc_endpoint: Optional[str],
    key_file: Optional[str],
    validator_addr_str: Optional[str],
    account: Optional[str],
) -> None:
    """
    Check the given validator for unclaimed-fees.
    """
    validator_addr = get_validator_address(validator_addr_str)
    account = from_address_from_argument(account, key_file)

    w3 = web3_from_endpoint_arg(None, rpc_endpoint)
    aut = Autonity(w3)
    vdesc = aut.get_validator(validator_addr)
    val = Validator(w3, vdesc)
    print(val.unclaimed_rewards(account))


validator.add_command(unclaimed_rewards)


@command()
@rpc_endpoint_option
@keyfile_option()
@from_option
@tx_aux_options
@validator_option
def claim_rewards(
    rpc_endpoint: Optional[str],
    key_file: Optional[str],
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
    validator_addr = get_validator_address(validator_addr_str)
    from_addr = from_address_from_argument(from_str, key_file)

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


validator.add_command(claim_rewards)

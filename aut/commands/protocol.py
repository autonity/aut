"""
The `protocol` command group.
"""

from typing import Any, Sequence

from autonity.autonity import AUTONITY_CONTRACT_ADDRESS, Autonity
from click import argument, command, echo, group
from web3 import Web3

from ..options import config_option, rpc_endpoint_option
from ..utils import to_json

# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals


@group(name="protocol")
def protocol_group() -> None:
    """Commands related to Autonity-specific protocol operations.

    See the Autonity contract reference for details.
    """


def _show_sequence(value: Sequence[Any]) -> str:
    return "\n".join([str(v) for v in value])


def _show_json(value: Any) -> str:

    return to_json(value, pretty=True)


@command()
@config_option
@rpc_endpoint_option
def commission_rate_precision(w3: Web3) -> None:
    """Precision of validator commission rate values."""

    print(Autonity(w3).commission_rate_precision())


protocol_group.add_command(commission_rate_precision)


@command()
@config_option
@rpc_endpoint_option
def max_bond_applied_gas(w3: Web3) -> None:
    """Max allowed gas for notifying delegator about bonding."""

    print(Autonity(w3).max_bond_applied_gas())


protocol_group.add_command(max_bond_applied_gas)


@command()
@config_option
@rpc_endpoint_option
def max_unbond_applied_gas(w3: Web3) -> None:
    """Max allowed gas for notifying delegator about unbonding."""

    print(Autonity(w3).max_unbond_applied_gas())


protocol_group.add_command(max_unbond_applied_gas)


@command()
@config_option
@rpc_endpoint_option
def max_unbond_released_gas(w3: Web3) -> None:
    """Max allowed gas for notifying delegator about bond being released."""

    print(Autonity(w3).max_unbond_released_gas())


protocol_group.add_command(max_unbond_released_gas)


@command()
@config_option
@rpc_endpoint_option
def max_rewards_distribution_gas(w3: Web3) -> None:
    """Max allowed gas for notifying delegator about rewards being distributed."""

    print(Autonity(w3).max_rewards_distribution_gas())


protocol_group.add_command(max_rewards_distribution_gas)


@command()
@config_option
@rpc_endpoint_option
def config(w3: Web3) -> None:
    """Print the Autonity contract config."""

    print(_show_json(Autonity(w3).config()))


protocol_group.add_command(config)


@command()
@config_option
@rpc_endpoint_option
def epoch_id(w3: Web3) -> None:
    """ID of current epoch."""

    print(Autonity(w3).epoch_id())


protocol_group.add_command(epoch_id)


@command()
@config_option
@rpc_endpoint_option
def last_epoch_time(w3: Web3) -> None:
    """Timestamp of the last epoch."""

    print(Autonity(w3).last_epoch_time())


protocol_group.add_command(last_epoch_time)


@command()
@config_option
@rpc_endpoint_option
def epoch_total_bonded_stake(w3: Web3) -> None:
    """Total stake bonded this epoch."""

    print(Autonity(w3).epoch_total_bonded_stake())


protocol_group.add_command(epoch_total_bonded_stake)


@command()
@config_option
@rpc_endpoint_option
def atn_total_redistributed(w3: Web3) -> None:
    """Total fees redistributed."""

    print(Autonity(w3).atn_total_redistributed())


protocol_group.add_command(atn_total_redistributed)


@command()
@config_option
@rpc_endpoint_option
def epoch_reward(w3: Web3) -> None:
    """Reward for this epoch."""

    print(Autonity(w3).epoch_reward())


protocol_group.add_command(epoch_reward)


@command()
@config_option
@rpc_endpoint_option
def staking_gas_price(w3: Web3) -> None:
    """The gas price to notify the delegator about the staking operation at epoch end."""

    print(Autonity(w3).staking_gas_price())


protocol_group.add_command(staking_gas_price)


@command()
@config_option
@rpc_endpoint_option
def inflation_reserve(w3: Web3) -> None:
    """The inflation reserve."""

    print(Autonity(w3).inflation_reserve())


protocol_group.add_command(inflation_reserve)


@command()
@config_option
@rpc_endpoint_option
def deployer(w3: Web3) -> None:
    """Contract deployer."""

    print(Autonity(w3).deployer())


protocol_group.add_command(deployer)


@command()
@config_option
@rpc_endpoint_option
def epoch_period(w3: Web3) -> None:
    """Epoch period in blocks."""

    print(Autonity(w3).get_epoch_period())


protocol_group.add_command(epoch_period)


@command()
@config_option
@rpc_endpoint_option
def block_period(w3: Web3) -> None:
    """Block period in seconds."""

    print(Autonity(w3).get_block_period())


protocol_group.add_command(block_period)


@command()
@config_option
@rpc_endpoint_option
def unbonding_period(w3: Web3) -> None:
    """Unbonding period in blocks."""

    print(Autonity(w3).get_unbonding_period())


protocol_group.add_command(unbonding_period)


@command()
@config_option
@rpc_endpoint_option
def last_epoch_block(w3: Web3) -> None:
    """Block number of the last epoch."""

    print(Autonity(w3).get_last_epoch_block())


protocol_group.add_command(last_epoch_block)


@command()
@config_option
@rpc_endpoint_option
def version(w3: Web3) -> None:
    """Contract version."""

    print(Autonity(w3).get_version())


protocol_group.add_command(version)


@command()
@config_option
@rpc_endpoint_option
def committee(w3: Web3) -> None:
    """Get current committee."""

    print(_show_json(Autonity(w3).get_committee()))


protocol_group.add_command(committee)


@command()
@config_option
@rpc_endpoint_option
def validators(w3: Web3) -> None:
    """Get current validators."""

    print(_show_sequence(Autonity(w3).get_validators()))


protocol_group.add_command(validators)


@command()
@config_option
@rpc_endpoint_option
def treasury_account(w3: Web3) -> None:
    """Treasury account address."""

    print(Autonity(w3).get_treasury_account())


protocol_group.add_command(treasury_account)


@command()
@config_option
@rpc_endpoint_option
def treasury_fee(w3: Web3) -> None:
    """Treasury fee."""

    print(Autonity(w3).get_treasury_fee())


protocol_group.add_command(treasury_fee)


@command()
@config_option
@rpc_endpoint_option
def max_committee_size(w3: Web3) -> None:
    """Maximum committee size."""

    print(Autonity(w3).get_max_committee_size())


protocol_group.add_command(max_committee_size)


@command()
@config_option
@rpc_endpoint_option
def committee_enodes(w3: Web3) -> None:
    """Enodes in current committee."""

    print(Autonity(w3).get_committee_enodes())


protocol_group.add_command(committee_enodes)


@command()
@config_option
@rpc_endpoint_option
def minimum_base_fee(w3: Web3) -> None:
    """Minimum base fee."""

    print(Autonity(w3).get_minimum_base_fee())


protocol_group.add_command(minimum_base_fee)


@command()
@config_option
@rpc_endpoint_option
def operator(w3: Web3) -> None:
    """The governance operator."""

    print(Autonity(w3).get_operator())


protocol_group.add_command(operator)


@command()
@config_option
@rpc_endpoint_option
@argument("height", type=int, nargs=1)
@argument("round_", metavar="ROUND", type=int, nargs=1)
def proposer(w3: Web3, height: int, round_: int) -> None:
    """Proposer at the given height and round."""

    print(Autonity(w3).get_proposer(height, round_))


protocol_group.add_command(proposer)


# -- Removed until https://github.com/autonity/autonity.py/pull/55 is released
# @command()
# @config_option
# @rpc_endpoint_option
# @argument("unbonding_id", type=int, nargs=1)
# def get_unbonding_release_state(w3: Web3, unbonding_id: int) -> None:
#     """Get the release state of the unbonding request."""
#     print(Autonity(w3).get_unbonding_release_state(unbonding_id))


# protocol_group.add_command(get_unbonding_release_state)


@command()
@config_option
@rpc_endpoint_option
@argument("unbonding_id", type=int, nargs=1)
def reverting_amount(w3: Web3, unbonding_id: int) -> None:
    """Get the amount of LNTN or NTN bonded when the released unbonding was reverted."""

    print(Autonity(w3).get_reverting_amount(unbonding_id))


protocol_group.add_command(reverting_amount)


@command()
@config_option
@rpc_endpoint_option
@argument("block", type=int, nargs=1)
def epoch_from_block(w3: Web3, block: int) -> None:
    """Get the epoch of the given block."""

    print(Autonity(w3).get_epoch_from_block(block))


protocol_group.add_command(epoch_from_block)


@command()
@config_option
def contract_address() -> None:
    """Address of the Autonity Contract."""

    echo(AUTONITY_CONTRACT_ADDRESS, nl=False)


protocol_group.add_command(contract_address)

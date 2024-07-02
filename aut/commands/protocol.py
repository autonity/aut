"""
The `protocol` command group.
"""

from typing import Any, Optional, Sequence

# from autonity import Autonity
from click import argument, command, echo, group

from aut.options import rpc_endpoint_option

# Disable pylint warning about imports outside top-level.  We do this
# intentionally to try and keep startup times of the CLI low.

# pylint: disable=import-outside-toplevel
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals


@group(name="protocol")
def protocol_group() -> None:
    """
    Commands related to Autonity-specific protocol operations.  See
    the Autonity contract reference for details.
    """


def _show_sequence(value: Sequence[Any]) -> str:
    return "\n".join([str(v) for v in value])


def _show_json(value: Any) -> str:
    from aut.utils import to_json

    return to_json(value, pretty=True)


@command()
@rpc_endpoint_option
def commission_rate_precision(rpc_endpoint: Optional[str]) -> None:
    """
    Precision of validator commission rate values
    """
    from aut.utils import autonity_from_endpoint_arg

    print(autonity_from_endpoint_arg(rpc_endpoint).commission_rate_precision())


protocol_group.add_command(commission_rate_precision)


@command()
@rpc_endpoint_option
def max_bond_applied_gas(rpc_endpoint: Optional[str]) -> None:
    """
    Max allowed gas for notifying delegator about bonding
    """
    from aut.utils import autonity_from_endpoint_arg

    print(autonity_from_endpoint_arg(rpc_endpoint).max_bond_applied_gas())


protocol_group.add_command(max_bond_applied_gas)


@command()
@rpc_endpoint_option
def max_unbond_applied_gas(rpc_endpoint: Optional[str]) -> None:
    """
    Max allowed gas for notifying delegator about unbonding
    """
    from aut.utils import autonity_from_endpoint_arg

    print(autonity_from_endpoint_arg(rpc_endpoint).max_unbond_applied_gas())


protocol_group.add_command(max_unbond_applied_gas)


@command()
@rpc_endpoint_option
def max_unbond_released_gas(rpc_endpoint: Optional[str]) -> None:
    """
    Max allowed gas for notifying delegator about bond being released
    """
    from aut.utils import autonity_from_endpoint_arg

    print(autonity_from_endpoint_arg(rpc_endpoint).max_unbond_released_gas())


protocol_group.add_command(max_unbond_released_gas)


@command()
@rpc_endpoint_option
def max_rewards_distribution_gas(rpc_endpoint: Optional[str]) -> None:
    """
    Max allowed gas for notifying delegator about rewards being distributed
    """
    from aut.utils import autonity_from_endpoint_arg

    print(autonity_from_endpoint_arg(rpc_endpoint).max_rewards_distribution_gas())


protocol_group.add_command(max_rewards_distribution_gas)


@command()
@rpc_endpoint_option
def config(rpc_endpoint: Optional[str]) -> None:
    """
    Print the Autonity contract config
    """
    from aut.utils import autonity_from_endpoint_arg

    print(_show_json(autonity_from_endpoint_arg(rpc_endpoint).config()))


protocol_group.add_command(config)


@command()
@rpc_endpoint_option
def epoch_id(rpc_endpoint: Optional[str]) -> None:
    """
    ID of current epoch
    """
    from aut.utils import autonity_from_endpoint_arg

    print(autonity_from_endpoint_arg(rpc_endpoint).epoch_id())


protocol_group.add_command(epoch_id)


@command()
@rpc_endpoint_option
def last_epoch_block(rpc_endpoint: Optional[str]) -> None:
    """
    Block number of the last epoch
    """
    from aut.utils import autonity_from_endpoint_arg

    print(autonity_from_endpoint_arg(rpc_endpoint).last_epoch_block())


protocol_group.add_command(last_epoch_block)


@command()
@rpc_endpoint_option
def last_epoch_time(rpc_endpoint: Optional[str]) -> None:
    """
    Timestamp of the last epoch
    """
    from aut.utils import autonity_from_endpoint_arg

    print(autonity_from_endpoint_arg(rpc_endpoint).last_epoch_time())


protocol_group.add_command(last_epoch_time)


@command()
@rpc_endpoint_option
def epoch_total_bonded_stake(rpc_endpoint: Optional[str]) -> None:
    """
    Total stake bonded this epoch
    """
    from aut.utils import autonity_from_endpoint_arg

    print(autonity_from_endpoint_arg(rpc_endpoint).epoch_total_bonded_stake())


protocol_group.add_command(epoch_total_bonded_stake)


@command()
@rpc_endpoint_option
def atn_total_redistributed(rpc_endpoint: Optional[str]) -> None:
    """
    Total fees redistributed
    """
    from aut.utils import autonity_from_endpoint_arg

    print(autonity_from_endpoint_arg(rpc_endpoint).atn_total_redistributed())


protocol_group.add_command(atn_total_redistributed)


@command()
@rpc_endpoint_option
def epoch_reward(rpc_endpoint: Optional[str]) -> None:
    """
    Reward for this epoch
    """
    from aut.utils import autonity_from_endpoint_arg

    print(autonity_from_endpoint_arg(rpc_endpoint).epoch_reward())


protocol_group.add_command(epoch_reward)


@command()
@rpc_endpoint_option
def staking_gas_price(rpc_endpoint: Optional[str]) -> None:
    """
    The gas price to notify the delegator about the staking operation at epoch end
    """
    from aut.utils import autonity_from_endpoint_arg

    print(autonity_from_endpoint_arg(rpc_endpoint).staking_gas_price())


protocol_group.add_command(staking_gas_price)


@command()
@rpc_endpoint_option
def inflation_reserve(rpc_endpoint: Optional[str]) -> None:
    """
    The inflation reserve
    """
    from aut.utils import autonity_from_endpoint_arg

    print(autonity_from_endpoint_arg(rpc_endpoint).inflation_reserve())


protocol_group.add_command(inflation_reserve)


@command()
@rpc_endpoint_option
def deployer(rpc_endpoint: Optional[str]) -> None:
    """
    Contract deployer
    """
    from aut.utils import autonity_from_endpoint_arg

    print(autonity_from_endpoint_arg(rpc_endpoint).deployer())


protocol_group.add_command(deployer)


@command()
@rpc_endpoint_option
def get_epoch_period(rpc_endpoint: Optional[str]) -> None:
    """Epoch period in blocks"""
    from aut.utils import autonity_from_endpoint_arg

    print(autonity_from_endpoint_arg(rpc_endpoint).get_epoch_period())


protocol_group.add_command(get_epoch_period)


@command()
@rpc_endpoint_option
def get_block_period(rpc_endpoint: Optional[str]) -> None:
    """Block period in seconds"""
    from aut.utils import autonity_from_endpoint_arg

    print(autonity_from_endpoint_arg(rpc_endpoint).get_block_period())


protocol_group.add_command(get_block_period)


@command()
@rpc_endpoint_option
def get_unbonding_period(rpc_endpoint: Optional[str]) -> None:
    """Unbonding period in blocks"""
    from aut.utils import autonity_from_endpoint_arg

    print(autonity_from_endpoint_arg(rpc_endpoint).get_unbonding_period())


protocol_group.add_command(get_unbonding_period)


@command()
@rpc_endpoint_option
def get_last_epoch_block(rpc_endpoint: Optional[str]) -> None:
    """
    Block of last epoch
    """
    from aut.utils import autonity_from_endpoint_arg

    print(autonity_from_endpoint_arg(rpc_endpoint).get_last_epoch_block())


protocol_group.add_command(get_last_epoch_block)


@command()
@rpc_endpoint_option
def get_version(rpc_endpoint: Optional[str]) -> None:
    """Contract version"""
    from aut.utils import autonity_from_endpoint_arg

    print(autonity_from_endpoint_arg(rpc_endpoint).get_version())


protocol_group.add_command(get_version)


@command()
@rpc_endpoint_option
def get_committee(rpc_endpoint: Optional[str]) -> None:
    """
    Get current committee
    """
    from aut.utils import autonity_from_endpoint_arg

    print(_show_json(autonity_from_endpoint_arg(rpc_endpoint).get_committee()))


protocol_group.add_command(get_committee)


@command()
@rpc_endpoint_option
def get_validators(rpc_endpoint: Optional[str]) -> None:
    """Get current validators"""
    from aut.utils import autonity_from_endpoint_arg

    print(_show_sequence(autonity_from_endpoint_arg(rpc_endpoint).get_validators()))


protocol_group.add_command(get_validators)


@command()
@rpc_endpoint_option
def get_treasury_account(rpc_endpoint: Optional[str]) -> None:
    """Treasury account address"""
    from aut.utils import autonity_from_endpoint_arg

    print(autonity_from_endpoint_arg(rpc_endpoint).get_treasury_account())


protocol_group.add_command(get_treasury_account)


@command()
@rpc_endpoint_option
def get_treasury_fee(rpc_endpoint: Optional[str]) -> None:
    """Treasury fee"""
    from aut.utils import autonity_from_endpoint_arg

    print(autonity_from_endpoint_arg(rpc_endpoint).get_treasury_fee())


protocol_group.add_command(get_treasury_fee)


@command()
@rpc_endpoint_option
def get_max_committee_size(rpc_endpoint: Optional[str]) -> None:
    """Maximum committee size"""
    from aut.utils import autonity_from_endpoint_arg

    print(autonity_from_endpoint_arg(rpc_endpoint).get_max_committee_size())


protocol_group.add_command(get_max_committee_size)


@command()
@rpc_endpoint_option
def get_committee_enodes(rpc_endpoint: Optional[str]) -> None:
    """Enodes in current committee"""
    from aut.utils import autonity_from_endpoint_arg

    print(autonity_from_endpoint_arg(rpc_endpoint).get_committee_enodes())


protocol_group.add_command(get_committee_enodes)


@command()
@rpc_endpoint_option
def get_minimum_base_fee(rpc_endpoint: Optional[str]) -> None:
    """Minimum base fee"""
    from aut.utils import autonity_from_endpoint_arg

    print(autonity_from_endpoint_arg(rpc_endpoint).get_minimum_base_fee())


protocol_group.add_command(get_minimum_base_fee)


@command()
@rpc_endpoint_option
def get_operator(rpc_endpoint: Optional[str]) -> None:
    """Contract operator"""
    from aut.utils import autonity_from_endpoint_arg

    print(autonity_from_endpoint_arg(rpc_endpoint).get_operator())


protocol_group.add_command(get_operator)


@command()
@rpc_endpoint_option
@argument("height", type=int, nargs=1)
@argument("round_", metavar="ROUND", type=int, nargs=1)
def get_proposer(rpc_endpoint: Optional[str], height: int, round_: int) -> None:
    """
    Proposer at the given height and round
    """
    from autonity import Autonity

    from aut.utils import web3_from_endpoint_arg

    aut = Autonity(web3_from_endpoint_arg(None, rpc_endpoint))
    print(aut.get_proposer(height, round_))


protocol_group.add_command(get_proposer)


# -- Removed until https://github.com/autonity/autonity.py/pull/55 is released
# @command()
# @rpc_endpoint_option
# @argument("unbonding_id", type=int, nargs=1)
# def get_unbonding_release_state(rpc_endpoint: Optional[str], unbonding_id: int) -> None:
#     """Get the release state of the unbonding request"""
#     from autonity import Autonity

#     from aut.utils import web3_from_endpoint_arg

#     aut = Autonity(web3_from_endpoint_arg(None, rpc_endpoint))
#     print(aut.get_unbonding_release_state(unbonding_id))


# protocol_group.add_command(get_unbonding_release_state)


@command()
@rpc_endpoint_option
@argument("unbonding_id", type=int, nargs=1)
def get_reverting_amount(rpc_endpoint: Optional[str], unbonding_id: int) -> None:
    """
    Get the amount of LNTN or NTN bonded when the released unbonding was reverted
    """
    from autonity import Autonity

    from aut.utils import web3_from_endpoint_arg

    aut = Autonity(web3_from_endpoint_arg(None, rpc_endpoint))
    print(aut.get_reverting_amount(unbonding_id))


protocol_group.add_command(get_reverting_amount)


@command()
@rpc_endpoint_option
@argument("block", type=int, nargs=1)
def get_epoch_from_block(rpc_endpoint: Optional[str], block: int) -> None:
    """Get the epoch of the given block"""
    from autonity import Autonity

    from aut.utils import web3_from_endpoint_arg

    aut = Autonity(web3_from_endpoint_arg(None, rpc_endpoint))
    print(aut.get_epoch_from_block(block))


protocol_group.add_command(get_epoch_from_block)


@command()
def contract_address() -> None:
    """
    Print the default Autonity contract address.
    """
    from autonity import AUTONITY_CONTRACT_ADDRESS

    echo(AUTONITY_CONTRACT_ADDRESS, nl=False)


protocol_group.add_command(contract_address)

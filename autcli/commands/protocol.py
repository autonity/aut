"""
The `autonity` command group.
"""

from autcli.options import rpc_endpoint_option

# from autonity import Autonity

from click import group, command, argument
from typing import Sequence, Optional, Any

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
    from autcli.utils import to_json

    return to_json(value, pretty=True)


@command()
@rpc_endpoint_option
def commission_rate_precision(rpc_endpoint: Optional[str]) -> None:
    """
    Precision of validator commission rate values
    """
    from autcli.utils import autonity_from_endpoint_arg

    print(autonity_from_endpoint_arg(rpc_endpoint).commission_rate_precision())


protocol_group.add_command(commission_rate_precision)


@command()
@rpc_endpoint_option
def config(rpc_endpoint: Optional[str]) -> None:
    """
    Print the Autonity contract config
    """
    from autcli.utils import autonity_from_endpoint_arg

    print(_show_json(autonity_from_endpoint_arg(rpc_endpoint).config()))


protocol_group.add_command(config)


@command()
@rpc_endpoint_option
def epoch_id(rpc_endpoint: Optional[str]) -> None:
    """
    ID of current epoch
    """
    from autcli.utils import autonity_from_endpoint_arg

    print(autonity_from_endpoint_arg(rpc_endpoint).epoch_id())


protocol_group.add_command(epoch_id)


@command()
@rpc_endpoint_option
def last_epoch_block(rpc_endpoint: Optional[str]) -> None:
    """
    Block number of the last epoch
    """
    from autcli.utils import autonity_from_endpoint_arg

    print(autonity_from_endpoint_arg(rpc_endpoint).last_epoch_block())


protocol_group.add_command(last_epoch_block)


@command()
@rpc_endpoint_option
def epoch_total_bonded_stake(rpc_endpoint: Optional[str]) -> None:
    """
    Total stake bonded this epoch
    """
    from autcli.utils import autonity_from_endpoint_arg

    print(autonity_from_endpoint_arg(rpc_endpoint).epoch_total_bonded_stake())


protocol_group.add_command(epoch_total_bonded_stake)


@command()
@rpc_endpoint_option
def total_redistributed(rpc_endpoint: Optional[str]) -> None:
    """
    Total fees redistributed
    """
    from autcli.utils import autonity_from_endpoint_arg

    print(autonity_from_endpoint_arg(rpc_endpoint).total_redistributed())


protocol_group.add_command(total_redistributed)


@command()
@rpc_endpoint_option
def epoch_reward(rpc_endpoint: Optional[str]) -> None:
    """
    Reward for this epoch
    """
    from autcli.utils import autonity_from_endpoint_arg

    print(autonity_from_endpoint_arg(rpc_endpoint).epoch_reward())


protocol_group.add_command(epoch_reward)


@command()
@rpc_endpoint_option
def tail_bonding_id(rpc_endpoint: Optional[str]) -> None:
    """Tail ID of bonding queue"""
    from autcli.utils import autonity_from_endpoint_arg

    print(autonity_from_endpoint_arg(rpc_endpoint).tail_bonding_id())


protocol_group.add_command(tail_bonding_id)


@command()
@rpc_endpoint_option
def head_bonding_id(rpc_endpoint: Optional[str]) -> None:
    """
    Head ID of bonding queue
    """
    from autcli.utils import autonity_from_endpoint_arg

    print(autonity_from_endpoint_arg(rpc_endpoint).head_bonding_id())


protocol_group.add_command(head_bonding_id)


@command()
@rpc_endpoint_option
def tail_unbonding_id(rpc_endpoint: Optional[str]) -> None:
    """
    Tail ID of unbondign queue
    """
    from autcli.utils import autonity_from_endpoint_arg

    print(autonity_from_endpoint_arg(rpc_endpoint).tail_unbonding_id())


protocol_group.add_command(tail_unbonding_id)


@command()
@rpc_endpoint_option
def head_unbonding_id(rpc_endpoint: Optional[str]) -> None:
    """
    Head ID of unbondign queue
    """
    from autcli.utils import autonity_from_endpoint_arg

    print(autonity_from_endpoint_arg(rpc_endpoint).head_unbonding_id())


protocol_group.add_command(head_unbonding_id)


@command()
@rpc_endpoint_option
def deployer(rpc_endpoint: Optional[str]) -> None:
    """
    Contract deployer
    """
    from autcli.utils import autonity_from_endpoint_arg

    print(autonity_from_endpoint_arg(rpc_endpoint).deployer())


protocol_group.add_command(deployer)


@command()
@rpc_endpoint_option
def get_last_epoch_block(rpc_endpoint: Optional[str]) -> None:
    """
    Block of last epoch
    """
    from autcli.utils import autonity_from_endpoint_arg

    print(autonity_from_endpoint_arg(rpc_endpoint).get_last_epoch_block())


protocol_group.add_command(get_last_epoch_block)


@command()
@rpc_endpoint_option
def get_version(rpc_endpoint: Optional[str]) -> None:
    """Contract version"""
    from autcli.utils import autonity_from_endpoint_arg

    print(autonity_from_endpoint_arg(rpc_endpoint).get_version())


protocol_group.add_command(get_version)


@command()
@rpc_endpoint_option
def get_committee(rpc_endpoint: Optional[str]) -> None:
    """
    Get current committee"
    """
    from autcli.utils import autonity_from_endpoint_arg

    print(_show_json(autonity_from_endpoint_arg(rpc_endpoint).get_committee()))


protocol_group.add_command(get_committee)


@command()
@rpc_endpoint_option
def get_validators(rpc_endpoint: Optional[str]) -> None:
    """Get current validators"""
    from autcli.utils import autonity_from_endpoint_arg

    print(_show_sequence(autonity_from_endpoint_arg(rpc_endpoint).get_validators()))


protocol_group.add_command(get_validators)


@command()
@rpc_endpoint_option
def get_max_committee_size(rpc_endpoint: Optional[str]) -> None:
    """Maximum committee size"""
    from autcli.utils import autonity_from_endpoint_arg

    print(autonity_from_endpoint_arg(rpc_endpoint).get_max_committee_size())


protocol_group.add_command(get_max_committee_size)


@command()
@rpc_endpoint_option
def get_committee_enodes(rpc_endpoint: Optional[str]) -> None:
    """Enodes in current committee"""
    from autcli.utils import autonity_from_endpoint_arg

    print(autonity_from_endpoint_arg(rpc_endpoint).get_committee_enodes())


protocol_group.add_command(get_committee_enodes)


@command()
@rpc_endpoint_option
def get_minimum_base_fee(rpc_endpoint: Optional[str]) -> None:
    """Minimum base fee"""
    from autcli.utils import autonity_from_endpoint_arg

    print(autonity_from_endpoint_arg(rpc_endpoint).get_minimum_base_fee())


protocol_group.add_command(get_minimum_base_fee)


@command()
@rpc_endpoint_option
def get_operator(rpc_endpoint: Optional[str]) -> None:
    """Contract operator"""
    from autcli.utils import autonity_from_endpoint_arg

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
    from autcli.utils import web3_from_endpoint_arg
    from autonity import Autonity

    aut = Autonity(web3_from_endpoint_arg(None, rpc_endpoint))
    print(aut.get_proposer(height, round_))


protocol_group.add_command(get_proposer)


@command()
@rpc_endpoint_option
@argument("start", type=int, nargs=1)
@argument("end", type=int, nargs=1)
def get_bonding_req(rpc_endpoint: Optional[str], start: int, end: int) -> None:
    """
    Get queued bonding information between start and end ids.
    """
    from autcli.utils import web3_from_endpoint_arg
    from autonity import Autonity

    aut = Autonity(web3_from_endpoint_arg(None, rpc_endpoint))
    print(_show_json(aut.get_bonding_req(start, end)))


protocol_group.add_command(get_bonding_req)


@command()
@rpc_endpoint_option
@argument("start", type=int, nargs=1)
@argument("end", type=int, nargs=1)
def get_unbonding_req(rpc_endpoint: Optional[str], start: int, end: int) -> None:
    """
    Get queued unbonding information between start and end ids.
    """
    from autcli.utils import web3_from_endpoint_arg
    from autonity import Autonity

    aut = Autonity(web3_from_endpoint_arg(None, rpc_endpoint))
    print(_show_json(aut.get_unbonding_req(start, end)))


protocol_group.add_command(get_unbonding_req)

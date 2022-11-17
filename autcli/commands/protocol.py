"""
The `autonity` command group.
"""

from autcli.options import rpc_endpoint_option
from autcli.utils import web3_from_endpoint_arg, to_json

from autonity import Autonity

from click import group, command, argument
from typing import Callable, Sequence, Optional, Any

# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals


@group(name="protocol")
def protocol_group() -> None:
    """
    Commands related to Autonity-specific protocol operations.  See
    the Autonity contract reference for details.
    """


GetMethod = Callable[[Autonity], Any]


def _show_sequence(value: Sequence[Any]) -> str:
    return "\n".join([str(v) for v in value])


def _show_json(value: Any) -> str:
    return to_json(value, pretty=True)


def _protocol_getter_command(
    name: str,
    method: GetMethod,
    comment: str,
    show: Optional[Callable[[Any], str]] = None,
) -> None:
    """
    Create an protocol method and register it.
    """

    @command(name=name, help=comment)
    @rpc_endpoint_option
    def cmd(rpc_endpoint: Optional[str]) -> None:
        aut = Autonity(web3_from_endpoint_arg(None, rpc_endpoint))
        ret = method(aut)
        if show:
            print(show(ret))
        else:
            print(ret)

    protocol_group.add_command(cmd)


_protocol_getter_command(
    "commission-rate-precision",
    Autonity.commission_rate_precision,
    "Precision of validator  commission rate values",
)
_protocol_getter_command(
    "config", Autonity.config, "Print the Autonity contract config", _show_json
)
_protocol_getter_command("epoch-id", Autonity.epoch_id, "ID of current epoch")
_protocol_getter_command(
    "last-epoch-block", Autonity.last_epoch_block, "block number of the last epoch"
)
_protocol_getter_command(
    "epoch-total-bonded-stake",
    Autonity.epoch_total_bonded_stake,
    "Total stake bonded this epoch",
)
_protocol_getter_command(
    "total-redistributed", Autonity.total_redistributed, "Total fees redistributed"
)
_protocol_getter_command("epoch-reward", Autonity.epoch_reward, "Reward for this epoch")
_protocol_getter_command(
    "tail-bonding-id", Autonity.tail_bonding_id, "Tail ID of bonding queue"
)
_protocol_getter_command(
    "head-bonding-id", Autonity.head_bonding_id, "Head ID of bonding queue"
)
_protocol_getter_command(
    "tail-unbonding-id", Autonity.tail_unbonding_id, "Tail ID of unbondign queue "
)
_protocol_getter_command(
    "head-unbonding-id", Autonity.head_unbonding_id, "Head ID of unbondign queue "
)
_protocol_getter_command("deployer", Autonity.deployer, "Contract deployer")
_protocol_getter_command(
    "get-last-epoch-block", Autonity.get_last_epoch_block, "Block of last epoch"
)
_protocol_getter_command("get-version", Autonity.get_version, "Contract version")
_protocol_getter_command(
    "get-committee", Autonity.get_committee, "Get current committee", _show_json
)
_protocol_getter_command(
    "get-validators", Autonity.get_validators, "Get current validators", _show_sequence
)

_protocol_getter_command(
    "get-max-committee-size", Autonity.get_max_committee_size, "Maximum committee size"
)
_protocol_getter_command(
    "get-committee-enodes", Autonity.get_committee_enodes, "Enodes in current committee"
)
_protocol_getter_command(
    "get-minimum-base-fee", Autonity.get_minimum_base_fee, "Minimum base fee"
)
_protocol_getter_command("get-operator", Autonity.get_operator, "Contract operator")


@command()
@rpc_endpoint_option
@argument("height", type=int, nargs=1)
@argument("round_", metavar="ROUND", type=int, nargs=1)
def get_proposer(rpc_endpoint: Optional[str], height: int, round_: int) -> None:
    """
    Proposer at the given height and round
    """
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
    aut = Autonity(web3_from_endpoint_arg(None, rpc_endpoint))
    print(_show_json(aut.get_unbonding_req(start, end)))


protocol_group.add_command(get_unbonding_req)

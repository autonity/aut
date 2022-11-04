"""
The `autonity` command group.
"""

from autcli.options import rpc_endpoint_option
from autcli.utils import web3_from_endpoint_arg, to_json

from autonity import Autonity

from web3 import Web3
from click import group, command, argument
from typing import Callable, Sequence, Optional, Any


@group()
def autonity() -> None:
    """
    Commands related to the Autonity contract.  See the Autonity
    contract reference for details.
    """


GetMethod = Callable[[Autonity], Any]


def _show_sequence(value: Sequence[Any]) -> str:
    return "\n".join([str(v) for v in value])


def _show_json(value: Any) -> str:
    return to_json(value, pretty=True)


def _autonity_getter_command(
    name: str,
    method: GetMethod,
    comment: str,
    show: Optional[Callable[[Any], str]] = None,
) -> None:
    """
    Create an autonity method and register it.
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

    autonity.add_command(cmd)


_autonity_getter_command(
    "config", Autonity.config, "Print the Autonity contract config", _show_json
)
_autonity_getter_command("epoch-id", Autonity.epoch_id, "ID of current epoch")
_autonity_getter_command(
    "last-epoch-block", Autonity.last_epoch_block, "block number of the last epoch"
)
_autonity_getter_command(
    "epoch-total-bonded-stake",
    Autonity.epoch_total_bonded_stake,
    "Total stake bonded this epoch",
)
_autonity_getter_command(
    "total-redistributed", Autonity.total_redistributed, "Total fees redistributed"
)
_autonity_getter_command("epoch-reward", Autonity.epoch_reward, "Reward for this epoch")
_autonity_getter_command(
    "tail-bonding-id", Autonity.tail_bonding_id, "Tail ID of bonding queue"
)
_autonity_getter_command(
    "head-bonding-id", Autonity.head_bonding_id, "Head ID of bonding queue"
)
_autonity_getter_command(
    "tail-unbonding-id", Autonity.tail_unbonding_id, "Tail ID of unbondign queue "
)
_autonity_getter_command(
    "head-unbonding-id", Autonity.head_unbonding_id, "Head ID of unbondign queue "
)
_autonity_getter_command("deployer", Autonity.deployer, "Contract deployer")
_autonity_getter_command(
    "get-last-epoch-block", Autonity.get_last_epoch_block, "Block of last epoch"
)
_autonity_getter_command("get-version", Autonity.get_version, "Contract version")
_autonity_getter_command(
    "get-committee", Autonity.get_committee, "Get current committee", _show_json
)
_autonity_getter_command(
    "get-validators", Autonity.get_validators, "Get current validators", _show_sequence
)


@command()
@rpc_endpoint_option
@argument("validator_address", nargs=1)
def get_validator(rpc_endpoint: Optional[str], validator_address: str) -> None:
    """
    Get the information about a specific validator.
    """
    addr = Web3.toChecksumAddress(validator_address)
    aut = Autonity(web3_from_endpoint_arg(None, rpc_endpoint))
    print(_show_json(aut.get_validator(addr)))


autonity.add_command(get_validator)


_autonity_getter_command(
    "get-max-committee-size", Autonity.get_max_committee_size, "Maximum committee size"
)
_autonity_getter_command(
    "get-committee-enodes", Autonity.get_committee_enodes, "Enodes in current committee"
)
_autonity_getter_command(
    "get-minimum-base-fee", Autonity.get_minimum_base_fee, "Minimum base fee"
)
_autonity_getter_command("get-operator", Autonity.get_operator, "Contract operator")


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


autonity.add_command(get_proposer)


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


autonity.add_command(get_bonding_req)


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


autonity.add_command(get_unbonding_req)

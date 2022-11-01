"""
The aut get command group
"""

from autonity import Autonity
from autonity.erc20 import ERC20

from autcli.utils import to_json, validate_block_identifier, web3_from_endpoint_arg
from autcli.options import rpc_endpoint_option
from autcli.user import get_account_stats, get_node_stats, get_block

import sys
from web3 import Web3
from click import group, command, option, argument, ClickException
from typing import List, Optional


@group()
def get() -> None:
    """
    Command group for getting blockchain information from the
    connected node.
    """


@command()
@rpc_endpoint_option
def stats(rpc_endpoint: Optional[str]) -> None:
    """
    Print general stats about RPC node and the blockchain it's on.
    """
    w3 = web3_from_endpoint_arg(None, rpc_endpoint)
    node_stats = get_node_stats(w3)
    print(to_json(node_stats))


@command()
@rpc_endpoint_option
@argument("identifier", default="latest")
def block(rpc_endpoint: Optional[str], identifier: str) -> None:
    """
    print information for block, where <identifier> is a block number or hash.
    """
    block_id = validate_block_identifier(identifier)
    w3 = web3_from_endpoint_arg(None, rpc_endpoint)
    block_data = get_block(w3, block_id)
    print(to_json(block_data))


@command()
@rpc_endpoint_option
@option(
    "--asof",
    help="state as of TAG, one of block number, 'latest', 'earliest', or 'pending'.",
)
@option(
    "--stdin",
    "use_stdin",
    is_flag=True,
    help="read account lines from stdin instead of positional arguments",
)
@argument("accounts", nargs=-1)
def account(
    rpc_endpoint: Optional[str],
    accounts: List[str],
    asof: Optional[str],
    use_stdin: bool,
) -> None:
    """
    print account tx count and balance state of one or more accounts.
    """

    if use_stdin:
        accounts = sys.stdin.read().splitlines()

    if len(accounts) == 0:
        print("No accounts specified")
        return

    addresses = [Web3.toChecksumAddress(act) for act in accounts]

    w3 = web3_from_endpoint_arg(None, rpc_endpoint)
    account_stats = get_account_stats(w3, addresses, asof)

    for acct, act_stats in account_stats.items():
        print(f"{acct} {act_stats[0]} {act_stats[1]}")


@command()
@rpc_endpoint_option
@option("--new", is_flag=True, help="print the Newton (NTN) balance instead of Auton")
@option("--token", help="print the balance of the ERC20 token at the given address")
@argument("account_str", metavar="ACCOUNT", nargs=1)
def balance(
    rpc_endpoint: Optional[str], account_str: str, new: bool, token: Optional[str]
) -> None:
    """
    Print the current balance of the given account.
    """
    account_addr = Web3.toChecksumAddress(account_str)
    w3 = web3_from_endpoint_arg(None, rpc_endpoint)

    if new:
        if token:
            raise ClickException(
                "cannot use --new and --token <addr> arguments together"
            )

        autonity = Autonity(w3)
        print(autonity.balance_of(account_addr))

    elif token:
        token_contract = ERC20(w3, Web3.toChecksumAddress(token))
        print(token_contract.balance_of(account_addr))

    else:
        print(w3.eth.get_balance(account_addr))


get.add_command(stats)
get.add_command(block)
get.add_command(account)
get.add_command(balance)

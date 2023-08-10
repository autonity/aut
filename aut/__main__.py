"""
Autonity RPC Client
"""

import sys

from click import group, option, version_option

from aut.commands import (
    account,
    block,
    contract,
    node,
    protocol,
    token,
    tx,
    validator,
)
from aut.logging import enable_logging


@group(context_settings=dict(help_option_names=["-h", "--help"]))
@option("--verbose", "-v", is_flag=True, help="Enable additional output (to stderr)")
@version_option()
def aut(verbose: bool) -> None:
    """
    Autonity Utility Tool.  RPC client and general toolbox for
    interacting with Autonity nodes.
    """

    if verbose:
        enable_logging()
    else:
        # Do not print the full callstack
        sys.tracebacklimit = 0


aut.add_command(node.node_group)
aut.add_command(block.block_group)
aut.add_command(tx.tx_group)
aut.add_command(protocol.protocol_group)
aut.add_command(validator.validator)
aut.add_command(account.account_group)
aut.add_command(token.token_group)
aut.add_command(contract.contract_group)

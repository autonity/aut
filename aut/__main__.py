"""
Autonity RPC Client
"""

import sys

from click import group, option, version_option

from aut import commands
from aut.lazy_group import LazyGroup
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


aut.add_command(commands.node_group)
aut.add_command(commands.block_group)
aut.add_command(commands.tx_group)
aut.add_command(commands.protocol_group)
aut.add_command(commands.validator_group)
aut.add_command(commands.account_group)
aut.add_command(commands.token_group)
aut.add_command(commands.contract_group)

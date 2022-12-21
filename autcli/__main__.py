"""
Autonity RPC Client
"""

from autcli.commands import (
    node,
    block,
    tx,
    protocol,
    validator,
    account,
    token,
)
from autcli.logging import enable_logging

import sys
from click import group, option, version_option


@group()
@option("--verbose", "-v", is_flag=True, help="Enable additional output (to stderr)")
@version_option()
def aut(verbose: bool) -> None:
    """
    Command line interface to Autonity functionality.
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


if __name__ == "__main__":
    aut()  # pylint: disable=no-value-for-parameter

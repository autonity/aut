"""
Autonity RPC Client
"""

from autcli.commands import (
    node,
    block,
    tx,
    autonity,
    validator,
    account,
)
from autcli.logging import enable_logging

from click import group, option


@group()
@option("--verbose", "-v", is_flag=True, help="Enable additional output (to stderr)")
def aut(verbose: bool) -> None:
    """
    Command line interface to Autonity functionality.
    """

    if verbose:
        enable_logging()


aut.add_command(node.node_group)
aut.add_command(block.block_group)
aut.add_command(tx.tx_group)
aut.add_command(autonity.autonity)
aut.add_command(validator.validator)
aut.add_command(account.account_group)


if __name__ == "__main__":
    aut()  # pylint: disable=no-value-for-parameter

"""
Autonity RPC Client
"""

from autcli.commands import maketx, signtx, sendtx, waittx, get, list as list_group
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


aut.add_command(maketx.maketx)
aut.add_command(signtx.signtx)
aut.add_command(sendtx.sendtx)
aut.add_command(waittx.waittx)
aut.add_command(get.get)
aut.add_command(list_group.list_group)

"""
Autonity RPC Client
"""

from autcli.commands import maketx, signtx, sendtx, waittx, get, list as list_group

from click import group


@group()
def aut() -> None:
    """
    Command line interface to Autonity functionality.
    """


aut.add_command(maketx.maketx)
aut.add_command(signtx.signtx)
aut.add_command(sendtx.sendtx)
aut.add_command(waittx.waittx)
aut.add_command(get.get)
aut.add_command(list_group.list_group)

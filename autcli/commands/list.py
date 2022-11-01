"""
The 'aut list' command group.
"""

from autcli.utils import address_keyfile_dict
from autcli import config

from click import group, command, option
from typing import Optional


@group(name="list")
def list_group() -> None:
    """
    Command group for enumerating local information.
    """


@command()
@option("--with-files", is_flag=True, help="also show keyfile names.")
@option(
    "--keystore",
    help="keystore directory (falls back to config file or ~/.autonity/keystore).",
)
def accounts(keystore: Optional[str], with_files: bool) -> None:
    """
    List the keys in a keyfile directory.
    """
    keystore = config.get_keystore_directory(keystore)
    keyfiles = address_keyfile_dict(keystore)
    for addr, keyfile in keyfiles.items():
        if with_files:
            print(addr + " " + keyfile)
        else:
            print(addr)


list_group.add_command(accounts)

"""
The `diagnostics` command group.
"""

from autcli.options import rpc_endpoint_option

from click import group, command, option, argument, Path
from typing import Optional

# Disable pylint warning about imports outside top-level.  We do this
# intentionally to try and keep startup times of the CLI low.

# pylint: disable=import-outside-toplevel
# pylint: disable=too-many-locals


@group(name="diagnostics")
def diagnostics_group() -> None:
    """
    Commands related to specific accounts.
    """


@command(name="generate-participants")
@option(
    "--num-participants",
    "-n",
    type=int,
    default=20,
    help="Number of fake participants to set up",
)
@option(
    "--seed",
    "-s",
    type=int,
    default=100,
    help="Number of fake participants to set up",
)
@argument("participants-file", type=Path())
def generate_participants_cmd(
    participants_file: str, num_participants: int, seed: int
) -> None:
    """
    Generate a set of fake participants FOR TESTING PURPOSES ONLY.
    Accounts are created using private keys with value `seed` up to
    `seed + num-participants`.  If running multiple instances of
    commands that use the participants file, ensure that each uses its
    own range of private keys, which does not overlap with any other
    instance.

    In order to use the participant set, one of the accounts must be
    funded (see the output from the command).
    """

    from autcli.utils import generate_participants

    import json

    participants = generate_participants(num_participants, seed)
    with open(participants_file, "w", encoding="utf8") as out_f:
        json.dump({k: v.hex() for k, v in participants.items()}, out_f)

    first_addr = next(iter(participants))
    print(f"Participants file written to: {participants_file}")
    print(f"Fund account: {first_addr}")


diagnostics_group.add_command(generate_participants_cmd)


@command()
@rpc_endpoint_option
@argument("participants-file", type=Path())
def generate_transactions(rpc_endpoint: Optional[str], participants_file: str) -> None:
    """
    Generate (and broadcast) a sequence of transactions between the
    participants in a file (generated via the `generate-participants`
    command).

    If multiple instances are executed at once, they must use
    completely disjoint participant sets.
    """

    from autcli import config
    from autcli.utils import generate_txs

    from autonity.utils.keyfile import PrivateKey

    from web3.types import HexBytes
    import json

    with open(participants_file, "r", encoding="utf8") as in_f:
        accounts_and_keys = {
            k: PrivateKey(HexBytes(v)) for k, v in json.load(in_f).items()
        }

    rpc_endpoint = config.get_rpc_endpoint(rpc_endpoint)
    generate_txs(rpc_endpoint, accounts_and_keys)


diagnostics_group.add_command(generate_transactions)

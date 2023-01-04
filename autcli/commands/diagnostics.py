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
    Generate a set of fake participants.
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
    Generate (and broadcast) a sequence of transactions to
    """

    from autcli import config
    from autcli.utils import (
        to_json,
        web3_from_endpoint_arg,
        from_address_from_argument_optional,
        generate_txs,
    )

    from autonity.utils.keyfile import PrivateKey

    from web3.types import HexBytes
    import json

    with open(participants_file, "r", encoding="utf8") as in_f:
        accounts_and_keys = {
            k: PrivateKey(HexBytes(v)) for k, v in json.load(in_f).items()
        }

    rpc_endpoint = config.get_rpc_endpoint(rpc_endpoint)
    w3 = web3_from_endpoint_arg(None, rpc_endpoint)

    generate_txs(rpc_endpoint, accounts_and_keys)


diagnostics_group.add_command(generate_transactions)

# @option(
#     "--asof",
#     help="state as of TAG, one of block number, 'latest', 'earliest', or 'pending'.",
# )
# @argument("accounts", nargs=-1)
# def info(
#     rpc_endpoint: Optional[str],
#     key_file: Optional[str],
#     accounts: List[str],
#     asof: Optional[str],
# ) -> None:
#     """
#     Print some information about the given account (falling back to
#     the default keyfile account if no accounts specified).
#     """

#     from autcli.user import get_account_stats
#     from autcli.utils import (
#         to_json,
#         web3_from_endpoint_arg,
#         from_address_from_argument_optional,
#     )

#     from web3 import Web3

#     if len(accounts) == 0:
#         account = from_address_from_argument_optional(None, key_file)
#         if not account:
#             raise ClickException("No accounts specified")
#         accounts = [account]

#     addresses = [Web3.toChecksumAddress(act) for act in accounts]

#     w3 = web3_from_endpoint_arg(None, rpc_endpoint)
#     account_stats = get_account_stats(w3, addresses, asof)
#     print(to_json(account_stats, pretty=True))


# account_group.add_command(info)


# @command()
# @rpc_endpoint_option
# @newton_or_token_option
# @keyfile_option()
# @argument("account_str", metavar="ACCOUNT", default="")
# def balance(
#     rpc_endpoint: Optional[str],
#     account_str: Optional[str],
#     key_file: Optional[str],
#     ntn: bool,
#     token: Optional[str],
# ) -> None:
#     """
#     Print the current balance of the given account.
#     """

#     from autcli.utils import (
#         web3_from_endpoint_arg,
#         newton_or_token_to_address,
#         from_address_from_argument_optional,
#     )

#     from autonity.erc20 import ERC20

#     account_addr = from_address_from_argument_optional(account_str, key_file)
#     if not account_addr:
#         raise ClickException(
#             "could not determine account address from argument or keyfile"
#         )

#     token_addresss = newton_or_token_to_address(ntn, token)

#     w3 = web3_from_endpoint_arg(None, rpc_endpoint)

#     # TODO: support printing in other denominations (AUT / units based
#     # on num decimals of token).

#     if token_addresss is not None:
#         token_contract = ERC20(w3, token_addresss)
#         print(token_contract.balance_of(account_addr))

#     else:
#         print(w3.eth.get_balance(account_addr))


# account_group.add_command(balance)


# @command()
# @rpc_endpoint_option
# @keyfile_option()
# @argument("account_str", metavar="ACCOUNT", default="")
# def lnew_balances(
#     rpc_endpoint: Optional[str], account_str: Optional[str], key_file: Optional[str]
# ) -> None:
#     """
#     Print the current balance of the given account.
#     """

#     from autcli.logging import log
#     from autcli.utils import (
#         to_json,
#         web3_from_endpoint_arg,
#         from_address_from_argument_optional,
#     )

#     from autonity.autonity import Autonity
#     from autonity.erc20 import ERC20

#     account_addr = from_address_from_argument_optional(account_str, key_file)
#     if not account_addr:
#         raise ClickException(
#             "could not determine account address from argument or keyfile"
#         )

#     w3 = web3_from_endpoint_arg(None, rpc_endpoint)
#     aut = Autonity(w3)
#     validator_addrs = aut.get_validators()
#     validators = [aut.get_validator(vaddr) for vaddr in validator_addrs]

#     balances: Dict[str, int] = {}
#     for validator in validators:
#         log("computing holdings for validators {validator['addr']}")
#         lnew = ERC20(w3, validator["liquid_contract"])
#         bal = lnew.balance_of(account_addr)
#         if bal:
#             balances[validator["addr"]] = bal

#     print(to_json(balances, pretty=True))


# account_group.add_command(lnew_balances)


# @command()
# @keyfile_option(required=True, output=True)
# @option(
#     "--extra-entropy",
#     is_flag=True,
#     help="Prompt the user for a string containing extra entropy",
# )
# @option(
#     "--show-password",
#     is_flag=True,
#     help="Echo password input to the terminal",
# )
# def new(key_file: str, extra_entropy: bool, show_password: bool) -> None:
#     """
#     Create a new key and write it to a keyfile.
#     """

#     from autcli.logging import log
#     from autcli.utils import prompt_for_new_password

#     from autonity.utils.keyfile import (
#         create_keyfile_from_private_key,
#         get_address_from_keyfile,
#     )

#     import json
#     import os.path
#     import eth_account

#     if os.path.exists(key_file):
#         raise ClickException("refusing to overwrite existing keyfile")

#     # Ask for extra entropy, if requested.

#     entropy: str = ""
#     if extra_entropy:
#         entropy = input("Entropy: ")

#     # Ask for password (and confirmation) and ensure both entries
#     # match.

#     password = prompt_for_new_password(show_password)
#     log("Generating private key ...")
#     account = eth_account.Account.create(entropy)
#     keyfile_data = create_keyfile_from_private_key(account.key, password)
#     keyfile_addr = get_address_from_keyfile(keyfile_data)
#     if account.address != keyfile_addr:
#         raise ClickException(
#             f"internal error (address-mismatch) {account.address} != {keyfile_addr}"
#         )

#     with open(key_file, "w", encoding="utf8") as key_f:
#         json.dump(keyfile_data, key_f)

#     log(f"Encrypted key written to {key_file}")

#     print(keyfile_addr)


# account_group.add_command(new)

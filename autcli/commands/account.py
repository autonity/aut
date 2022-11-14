"""
The `account` command group.
"""

from autcli import config
from autcli.logging import log
from autcli.options import rpc_endpoint_option, newton_or_token_option, keyfile_option
from autcli.user import get_account_stats
from autcli.utils import (
    address_keyfile_dict,
    to_json,
    web3_from_endpoint_arg,
    newton_or_token_to_address,
    from_address_from_argument_optional,
)

from autonity.utils.keyfile import (
    create_keyfile_from_private_key,
    get_address_from_keyfile,
)
from autonity.autonity import Autonity
from autonity.erc20 import ERC20

import sys
import os.path
import eth_account
import json
from getpass import getpass
from web3 import Web3
from click import group, command, option, argument, ClickException
from typing import Dict, List, Optional


@group(name="account")
def account_group() -> None:
    """
    Commands related to specific accounts.
    """


@command(name="list")
@option("--with-files", is_flag=True, help="also show keyfile names.")
@option(
    "--keystore",
    help="keystore directory (falls back to config file or ~/.autonity/keystore).",
)
def list_cmd(keystore: Optional[str], with_files: bool) -> None:
    """
    List the accounts for files in the keystore directory.
    """
    keystore = config.get_keystore_directory(keystore)
    keyfiles = address_keyfile_dict(keystore)
    for addr, keyfile in keyfiles.items():
        if with_files:
            print(addr + " " + keyfile)
        else:
            print(addr)


account_group.add_command(list_cmd)


@command()
@rpc_endpoint_option
@keyfile_option()
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
def info(
    rpc_endpoint: Optional[str],
    key_file: Optional[str],
    accounts: List[str],
    asof: Optional[str],
    use_stdin: bool,
) -> None:
    """
    Print some information about the given account.
    """

    if use_stdin:
        accounts = sys.stdin.read().splitlines()
    else:
        if len(accounts) == 0:
            account = from_address_from_argument_optional(None, key_file)
            if not account:
                raise ClickException("No accounts specified")
            accounts = [account]

    addresses = [Web3.toChecksumAddress(act) for act in accounts]

    w3 = web3_from_endpoint_arg(None, rpc_endpoint)
    account_stats = get_account_stats(w3, addresses, asof)
    print(to_json(account_stats, pretty=True))


account_group.add_command(info)


@command()
@rpc_endpoint_option
@newton_or_token_option
@keyfile_option()
@argument("account_str", metavar="ACCOUNT", default="")
def balance(
    rpc_endpoint: Optional[str],
    account_str: Optional[str],
    key_file: Optional[str],
    ntn: bool,
    token: Optional[str],
) -> None:
    """
    Print the current balance of the given account.
    """
    account_addr = from_address_from_argument_optional(account_str, key_file)
    if not account_addr:
        raise ClickException(
            "could not determine account address from argument or keyfile"
        )

    token_addresss = newton_or_token_to_address(ntn, token)

    w3 = web3_from_endpoint_arg(None, rpc_endpoint)

    # TODO: support printing in other denominations (AUT / units based
    # on num decimals of token).

    if token_addresss is not None:
        token_contract = ERC20(w3, token_addresss)
        print(token_contract.balance_of(account_addr))

    else:
        print(w3.eth.get_balance(account_addr))


account_group.add_command(balance)


@command()
@rpc_endpoint_option
@keyfile_option()
@argument("account_str", metavar="ACCOUNT", default="")
def lnew_balances(
    rpc_endpoint: Optional[str], account_str: Optional[str], key_file: Optional[str]
) -> None:
    """
    Print the current balance of the given account.
    """
    account_addr = from_address_from_argument_optional(account_str, key_file)
    if not account_addr:
        raise ClickException(
            "could not determine account address from argument or keyfile"
        )

    w3 = web3_from_endpoint_arg(None, rpc_endpoint)
    aut = Autonity(w3)
    validator_addrs = aut.get_validators()
    validators = [aut.get_validator(vaddr) for vaddr in validator_addrs]

    balances: Dict[str, int] = {}
    for validator in validators:
        log("computing holdings for validators {validator['addr']}")
        lnew = ERC20(w3, validator["liquid_contract"])
        bal = lnew.balance_of(account_addr)
        if bal:
            balances[validator["addr"]] = bal

    print(to_json(balances, pretty=True))


account_group.add_command(lnew_balances)


@command()
@keyfile_option(required=True)
@option(
    "--extra-entropy",
    is_flag=True,
    help="Prompt the user for a string containing extra entropy",
)
@option(
    "--show-password",
    is_flag=True,
    help="Echo password input to the terminal",
)
def new(key_file: str, extra_entropy: bool, show_password: bool) -> None:
    """
    Create a new key and write it to a keyfile.
    """

    if os.path.exists(key_file):
        raise ClickException("refusing to overwrite existing keyfile")

    # Ask for extra entropy, if requested.

    entropy: str = ""
    if extra_entropy:
        entropy = input("Entropy: ")

    # Ask for password (and confirmation) and ensure both entries
    # match.

    prompt = "Password for new account: "
    prompt_2 = "Confirm account password: "
    if show_password:
        password = input(prompt)
        password_2 = input(prompt_2)
    else:
        password = getpass(prompt)
        password_2 = getpass(prompt_2)

    if password != password_2:
        raise ClickException("passwords do not match")

    log("Generating private key ...")
    account = eth_account.Account.create(entropy)
    keyfile_data = create_keyfile_from_private_key(account.key, password)
    keyfile_addr = get_address_from_keyfile(keyfile_data)
    if account.address != keyfile_addr:
        raise ClickException(
            f"internal error (address-mismatch) {account.address} != {keyfile_addr}"
        )

    with open(key_file, "w", encoding="utf8") as key_f:
        json.dump(keyfile_data, key_f)

    log(f"Encrypted key written to {key_file}")

    print(keyfile_addr)


account_group.add_command(new)

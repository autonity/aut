"""
The `account` command group.
"""

import json
from typing import Dict, List, Optional

import eth_account
from autonity.autonity import Autonity
from autonity.erc20 import ERC20
from autonity.utils.denominations import (
    format_auton_quantity,
    format_newton_quantity,
    format_quantity,
)
from autonity.utils.keyfile import (
    PrivateKey,
    create_keyfile_from_private_key,
    decrypt_keyfile,
    get_address_from_keyfile,
)
from autonity.utils.tx import sign_tx
from click import ClickException, Path, argument, command, group, option
from eth_account import Account
from eth_account.messages import encode_defunct
from hexbytes import HexBytes
from web3 import Web3
from web3.types import BlockIdentifier

from ..logging import log
from ..options import (
    config_option,
    from_option,
    keyfile_and_password_options,
    keyfile_option,
    keystore_option,
    new_password_option,
    newton_or_token_option,
    rpc_endpoint_option,
)
from ..user import get_account_stats
from ..utils import (
    address_keyfile_dict,
    from_address_from_argument_optional,
    load_from_file_or_stdin,
    load_from_file_or_stdin_line,
    new_keyfile_from_options,
    newton_or_token_to_address,
    to_json,
    web3_from_endpoint_arg,
)

# pylint: disable=too-many-locals


@group(name="account")
def account_group() -> None:
    """Commands related to specific accounts."""


@command(name="list")
@config_option
@option("--with-files", is_flag=True, help="Show key file names.")
@keystore_option
def list_cmd(keystore: Optional[str], with_files: bool) -> None:
    """List the accounts for files in the keystore directory."""

    keyfiles = address_keyfile_dict(keystore)
    for addr, keyfile in keyfiles.items():
        if with_files:
            print(addr + " " + keyfile)
        else:
            print(addr)


account_group.add_command(list_cmd)


@command()
@config_option
@rpc_endpoint_option
@keyfile_option()
@option(
    "--asof",
    metavar="TAG",
    help="State as of TAG, one of block number, 'latest', 'earliest', or 'pending'.",
)
@argument("accounts", nargs=-1)
def info(
    rpc_endpoint: Optional[str],
    keyfile: Optional[str],
    accounts: List[str],
    asof: Optional[BlockIdentifier],
) -> None:
    """Print some information about the given account.

    Falls back to the default keyfile account if no accounts specified.
    """

    if len(accounts) == 0:
        account = from_address_from_argument_optional(None, keyfile)
        if not account:
            raise ClickException("No accounts specified")
        accounts = [account]

    addresses = [Web3.to_checksum_address(act) for act in accounts]

    w3 = web3_from_endpoint_arg(None, rpc_endpoint)
    account_stats = get_account_stats(w3, addresses, asof)
    print(to_json(account_stats, pretty=True))


account_group.add_command(info)


@command()
@config_option
@rpc_endpoint_option
@newton_or_token_option
@keyfile_option()
@argument("account_str", metavar="ACCOUNT", default="")
def balance(
    rpc_endpoint: Optional[str],
    account_str: Optional[str],
    keyfile: Optional[str],
    ntn: bool,
    token: Optional[str],
) -> None:
    """Print the current balance of the given account."""

    account_addr = from_address_from_argument_optional(account_str, keyfile)
    if not account_addr:
        raise ClickException(
            "Could not determine account address from argument or keyfile"
        )

    token_addresss = newton_or_token_to_address(ntn, token)

    w3 = web3_from_endpoint_arg(None, rpc_endpoint)

    # TODO: support printing in other denominations (AUT / units based
    # on num decimals of token).

    if ntn:
        autonity = Autonity(w3)
        print(format_newton_quantity(autonity.balance_of(account_addr)))

    elif token_addresss is not None:
        token_contract = ERC20(w3, token_addresss)
        decimals = token_contract.decimals()
        bal = token_contract.balance_of(account_addr)
        print(format_quantity(bal, decimals))

    else:
        print(format_auton_quantity(w3.eth.get_balance(account_addr)))


account_group.add_command(balance)


@command()
@config_option
@rpc_endpoint_option
@keyfile_option()
@argument("account_str", metavar="ACCOUNT", default="")
def lntn_balances(
    rpc_endpoint: Optional[str], account_str: Optional[str], keyfile: Optional[str]
) -> None:
    """Print all Liquid Newton balances of the given account."""

    account_addr = from_address_from_argument_optional(account_str, keyfile)
    if not account_addr:
        raise ClickException(
            "Could not determine account address from argument or keyfile"
        )

    w3 = web3_from_endpoint_arg(None, rpc_endpoint)
    aut = Autonity(w3)
    validator_addrs = aut.get_validators()
    validators = [aut.get_validator(vaddr) for vaddr in validator_addrs]

    balances: Dict[str, str] = {}
    for validator in validators:
        log(f"computing holdings for validators {validator['node_address']}")
        lntn = ERC20(w3, validator["liquid_contract"])
        bal = lntn.balance_of(account_addr)
        if bal:
            balances[validator["node_address"]] = format_newton_quantity(bal)

    print(to_json(balances, pretty=True))


account_group.add_command(lntn_balances)


@command()
@config_option
@keystore_option
@keyfile_option(required=False, output=True)
@new_password_option
@option(
    "--extra-entropy",
    type=Path(),
    help="File containing extra entropy. Use '-' to prompt for keyboard input.",
)
def new(
    keystore: Optional[str],
    keyfile: Optional[str],
    password: str,
    extra_entropy: Optional[str],
) -> None:
    """Create a new key and write it to a keyfile.

    If no keyfile is specified, a default name is used (consistent with GETH keyfiles)
    in the keystore.
    """

    # Ask for extra entropy, if requested.

    entropy: str = ""
    if extra_entropy:
        if extra_entropy == "-":
            entropy = input("Random string (press ENTER to finish): ")
        else:
            # Use ascii so that binary data is not reinterpreted.
            with open(extra_entropy, "r", encoding="ascii") as entropy_f:
                entropy = entropy_f.read()

    # Ask for password (and confirmation) and ensure both entries
    # match.

    log("Generating private key ...")
    account = eth_account.Account.create(entropy)
    keyfile_data = create_keyfile_from_private_key(account.key, password)
    keyfile_addr = get_address_from_keyfile(keyfile_data)
    if account.address != keyfile_addr:
        raise ClickException(
            f"internal error (address-mismatch) {account.address} != {keyfile_addr}"
        )

    # If keyfile was not given, generate a new keyfile based on
    # keystore and the new key details.
    keyfile = new_keyfile_from_options(keystore, keyfile, keyfile_addr)
    with open(keyfile, "w", encoding="utf8") as key_f:
        json.dump(keyfile_data, key_f)

    log(f"Encrypted key written to {keyfile}")

    print(f"{keyfile_addr}  {keyfile}")


account_group.add_command(new)


@command()
@config_option
@keystore_option
@keyfile_option(output=True)
@new_password_option
@argument("private_key_file", type=Path(exists=False))
def import_private_key(
    keystore: Optional[str],
    keyfile: Optional[str],
    password: str,
    private_key_file: str,
) -> None:
    """Read a plaintext private key file (as hex), and create a new encrypted keystore
    file for it.

    Use - to read private key from stdin. If no keyfile is specified, a default name is
    used (consistent with GETH keyfiles) in the keystore.
    """

    private_key = HexBytes.fromhex(load_from_file_or_stdin_line(private_key_file))
    if len(private_key) != 32:
        raise ClickException("invalid private key length")

    keyfile_data = create_keyfile_from_private_key(PrivateKey(private_key), password)
    keyfile_addr = get_address_from_keyfile(keyfile_data)

    keyfile = new_keyfile_from_options(keystore, keyfile, keyfile_addr)
    with open(keyfile, "w", encoding="utf8") as key_f:
        json.dump(keyfile_data, key_f)

    log(f"Encrypted key written to {keyfile}")

    keyfile_addr = get_address_from_keyfile(keyfile_data)
    print(f"{keyfile_addr}  {keyfile}")


account_group.add_command(import_private_key)


@command()
@config_option
@keyfile_and_password_options()
@argument(
    "tx-file",
    type=Path(),
    required=True,
)
def signtx(keyfile: Optional[str], password: str, tx_file: str) -> None:
    """Sign a transaction using the given keyfile.

    Use '-' to read from stdin instead of a file.

    If password is not given, the environment variable 'AUT_PASSWORD' is used.
    If that is not set, the user is prompted.
    """

    # Read tx
    tx = json.loads(load_from_file_or_stdin(tx_file))

    # Read keyfile
    log(f"using key file: {keyfile}")
    with open(keyfile, encoding="ascii") as key_f:
        encrypted_key = json.load(key_f)

    # Sign the tx:
    signed_tx = sign_tx(tx, encrypted_key, password)

    print(to_json(signed_tx._asdict()))


account_group.add_command(signtx)


@command()
@config_option
@keyfile_and_password_options()
@option(
    "--use-message-file",
    "-f",
    is_flag=True,
    help="Read message from a file. Use '-' to read message from stdin.",
)
@argument(
    "message",
    type=Path(),
)
@argument("signature-file", type=Path(), required=False)
def sign_message(
    keyfile: Optional[str],
    password: str,
    use_message_file: bool,
    message: str,
    signature_file: Optional[str],
) -> None:
    """Use the private key in the given keyfile to sign a message.

    MESSAGE may be a string or the contents of a file; see --use-message-file. The
    signature is always written to stdout (which can be piped to a
    file). The signature is also written to SIGNATURE_FILE, if given.
    """

    # Read message
    if use_message_file:
        message = load_from_file_or_stdin(message)

    # Read keyfile
    log(f"using key file: {keyfile}")
    with open(keyfile, encoding="ascii") as key_f:
        encrypted_key = json.load(key_f)

    # Read password
    private_key = decrypt_keyfile(encrypted_key, password)

    # Sign the message
    signature_data = Account().sign_message(
        signable_message=encode_defunct(text=message), private_key=private_key
    )
    signature = signature_data["signature"].hex()

    # Optionally write to the output file
    if signature_file:
        with open(signature_file, "w", encoding="ascii") as signature_f:
            signature_f.write(signature)

    print(signature)


account_group.add_command(sign_message)


@command()
@config_option
@keyfile_option()
@from_option
@option(
    "--use-message-file",
    "-f",
    is_flag=True,
    help="Read message from a file. Use '-' to read message from stdin.",
)
@argument(
    "message",
    type=Path(),
    required=True,
)
@argument(
    "signature-file",
    type=Path(),
    required=True,
)
def verify_signature(
    keyfile: Optional[str],
    from_str: Optional[str],
    use_message_file: bool,
    message: str,
    signature_file: str,
) -> None:
    """Verify that the signature of a message is valid.

    Verify that the signature in `SIGNATURE_FILE` is valid for the
    message MESSAGE, signed by the owner of the FROM address.
    Signature must be contained in a file.
    """

    if use_message_file:
        message = load_from_file_or_stdin(message)

    with open(signature_file, "r", encoding="ascii") as signature_f:
        # TODO: check file size before blindly reading everything
        signature_hex = signature_f.read().rstrip()
        signature = HexBytes(signature_hex)

    from_addr = from_address_from_argument_optional(from_str, keyfile)

    recovered_addr = Account().recover_message(
        encode_defunct(text=message), signature=signature
    )

    if recovered_addr != from_addr:
        log(f"recovered address was {recovered_addr}, not {from_addr}")
        raise ClickException("Signature invalid")

    log("signature is valid")


account_group.add_command(verify_signature)

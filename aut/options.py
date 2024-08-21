"""
Command line option sets used by multiple commands.
"""

from os import path
from typing import Any, Callable, TypeVar

from click import Path, option

from .config import config_file, read_defaults_from_config

Func = TypeVar("Func", bound=Callable[..., Any])

Decorator = Callable[[Func], Func]


def config_option(fn: Func) -> Func:
    """
    Option: --config <file>
    """
    # Based on https://jwodder.github.io/kbits/posts/click-config/
    return option(
        "--config",
        "-c",
        type=Path(exists=True),
        help="Read option defaults from the specified INI file.",
        default=config_file,
        callback=read_defaults_from_config,
        expose_value=False,
        is_eager=True,
    )(fn)


def rpc_endpoint_option(fn: Func) -> Func:
    """
    An --rpc-endpoint, -r <url> option
    """
    return option(
        "--rpc-endpoint",
        "-r",
        metavar="URL",
        help="RPC endpoint.",
        required=True,
    )(fn)


def keystore_option(fn: Func) -> Func:
    """
    Option: --keystore <directory>.
    """

    return option(
        "--keystore",
        "-s",
        type=Path(exists=True),
        default=path.join(path.expanduser("~"), ".autonity", "keystore"),
        help="Keystore directory.",
    )(fn)


def keyfile_option(required: bool = False, exists: bool = True) -> Decorator:
    """
    Options: --keyfile. If `required` is True, --keyfile is
    required. If `exists` is True, the file needs to exist.
    """

    def decorator(fn: Func) -> Func:
        return option(
            "--keyfile",
            "-k",
            required=required,
            type=Path(exists=exists),
            help="Encrypted private key file.",
        )(fn)

    return decorator


def keyfile_and_password_options(fn: Func) -> Func:
    """
    Options: --keyfile and --password.  If `required` is True,
    --keyfile is required.
    """

    fn = keyfile_option(required=True)(fn)
    fn = option(
        "--password",
        "-p",
        help="Password for key file.",
        prompt="Enter passphrase for key file",
        hide_input=True,
        show_default=False,
    )(fn)
    return fn


def new_password_option(fn: Func) -> Func:
    return option(
        "--password",
        "-p",
        help="Password for key file.",
        prompt="Key file passphrase for new account",
        confirmation_prompt=True,
        hide_input=True,
        show_default=False,
    )(fn)


def newton_or_token_option(fn: Func) -> Func:
    """
    Adds the --ntn and --token flags, allowing the user to specify
    that a transfer should use an ERC20 token.
    """
    fn = option("--ntn", is_flag=True, help="Use Newton (NTN) instead of Auton (ATN).")(
        fn
    )
    fn = option(
        "--token",
        "-t",
        metavar="TOKEN-ADDR",
        help="Use the ERC20 token at the given address.",
    )(fn)
    return fn


def from_option(fn: Func) -> Func:
    """
    Adds the --from, -f option to specify the from field of a
    transaction. Passed to the from_str parameter.
    """
    return option(
        "--from",
        "-f",
        "from_str",
        metavar="FROM",
        help="The from address (extracted from keyfile if not given).",
    )(fn)


def tx_value_option(required: bool = False) -> Decorator:
    """
    Adds the --value, -v option to specify tx value field.  If `required` is True, the
    value must be provided.
    """

    def decorator(fn: Func) -> Func:
        return option(
            "--value",
            "-v",
            required=required,
            help=(
                "Value in ATN or whole tokens with units "
                "(e.g. '0.000000007' and '7gwei' are identical)."
            ),
        )(fn)

    return decorator


def tx_aux_options(fn: Callable) -> Callable:
    """
    Remaining options which may be specified for any transaction.
      --gas
      --gas-price
      --max-fee-per-gas
      --max-priority-fee-per-gas
      --fee-factor,
      --nonce
      --chain-id
    """
    fn = option(
        "--gas", "-g", help="Maximum gas units that can be consumed by the tx."
    )(fn)
    fn = option(
        "--gas-price",
        "-p",
        help=(
            "Value per gas in ATN "
            "(legacy, use --max-fee-per-gas and --max-priority-fee-per-gas instead)."
        ),
    )(fn)
    fn = option(
        "--max-fee-per-gas",
        "-F",
        help="Maximum to pay (in ATN) per gas for the total fee of the tx.",
    )(fn)
    fn = option(
        "--max-priority-fee-per-gas",
        "-P",
        help="Maximum to pay (in ATN) per gas as tip to block proposer.",
    )(fn)
    fn = option(
        "--fee-factor",
        type=float,
        help="Sets --max-fee-per-gas to <last-base-fee> x <fee-factor>.",
    )(fn)
    fn = option(
        "--nonce",
        "-n",
        type=int,
        help="Tx nonce; the account's tx count is queried if not given.",
    )(fn)
    fn = option(
        "--chain-id",
        "-I",
        type=int,
        help="EIP155 chain ID.",
    )(fn)

    return fn


def validator_option(fn: Func) -> Func:
    """
    Add the --validator <address> option to specify a validator.  Uses
    the "validator_addr_str" argument.
    """
    return option(
        "--validator",
        "-V",
        "validator_addr_str",
        help="Validator address.",
        required=True,
    )(fn)


def contract_options(fn: Func) -> Func:
    """
    add the `--abi <contract_abi>` and `--address <contract_address>`
    options.
    """
    fn = option(
        "--address",
        "contract_address_str",
        help="Contract address.",
        required=True,
    )(fn)
    fn = option(
        "--abi",
        "contract_abi_path",
        type=Path(exists=True),
        help="Contract ABI file.",
        required=True,
    )(fn)
    return fn

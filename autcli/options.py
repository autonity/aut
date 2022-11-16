"""
Command line option sets used by multiple commands.
"""

from click import option
from typing import Callable, TypeVar, Any


Func = TypeVar("Func", bound=Callable[..., Any])

Decorator = Callable[[Func], Func]


# an --rpc-endpoint, -r <url> option
rpc_endpoint_option: Decorator = option(
    "--rpc-endpoint",
    "-r",
    metavar="URL",
    help="RPC endpoint (defaults to WEB3_ENDPOINT env var if set)",
)


def keyfile_option(required: bool = False) -> Decorator:
    """
    Options: --key-file.  If `required` is True, --key-file is
    required.
    """

    def decorator(fn: Func) -> Func:
        fn = option(
            "--key-file", "-k", required=required, help="Encrypted private key file"
        )(fn)
        return fn

    return decorator


def keyfile_and_password_options(required: bool = False) -> Decorator:
    """
    Options: --key-file and --password.  If `required` is True,
    --key-file is required.
    """

    def decorator(fn: Func) -> Func:
        fn = keyfile_option(required)(fn)
        fn = option(
            "--password",
            "-p",
            help="Password for key file (or use env var 'KEYFILEPWD')",
        )(fn)
        return fn

    return decorator


def newton_or_token_option(fn: Func) -> Func:
    """
    Adds the --ntn and --token flags, allowing the user to specify
    that a transfer should use an ERC20 token.
    """
    fn = option("--ntn", is_flag=True, help="Use Newton (NTN) instead of Auton")(fn)
    fn = option(
        "--token",
        "-t",
        metavar="TOKEN-ADDR",
        help="Use the ERC20 token at the given address",
    )(fn)
    return fn


def from_option(fn: Func) -> Func:
    """
    Adds the --from, -f option to specify the from field of a
    transaction.  Passed to the from_str parameter.
    """
    return option(
        "--from",
        "-f",
        "from_str",
        help="address from which tx is sent (extracted from keyfile if not given).",
    )(fn)


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
        "--gas", "-g", help="maximum gas units that can be consumed by the tx."
    )(fn)
    fn = option(
        "--gas-price",
        "-p",
        help="value per gas (legacy, use -F and -P instead).",
    )(fn)
    fn = option(
        "--max-fee-per-gas",
        "-F",
        help="maximum to pay per gas for the total fee of the tx.",
    )(fn)
    fn = option(
        "--max-priority-fee-per-gas",
        "-P",
        help="maximum to pay per gas as tip to block proposer.",
    )(fn)
    fn = option(
        "--fee-factor",
        type=float,
        help="set maxFeePerGas to <last-basefee> x <fee-factor> [default: 2].",
    )(fn)
    fn = option(
        "--nonce",
        "-n",
        type=int,
        help="tx nonce; query chain for account tx count if not given.",
    )(fn)
    fn = option(
        "--chain-id",
        "-I",
        type=int,
        help="integer representing EIP155 chainId.",
    )(fn)

    return fn


def validator_option(fn: Func) -> Func:
    """
    Add the --validator <address> option to specify a validator.  Uses
    the "validator_addr_str" argument.
    """
    return option(
        "--validator",
        "validator_addr_str",
        help="Validator address (defaults to value in config file)",
    )(fn)

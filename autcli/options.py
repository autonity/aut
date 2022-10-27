"""
Command line option sets used by multiple commands.
"""

from click import option
from typing import Callable, TypeVar, Any


Func = TypeVar("Func", bound=Callable[..., Any])

Decorator = Callable[[Func], Func]


# an --rpc-endpoint, -r <url> option
rpc_endpoint_option: Decorator = option(
    "--rpc-endpoint", "-r", help="RPC endpoint (defaults to WEB3_ENDPOINT env var"
)


def keyfile_and_password_options(required: bool = False) -> Decorator:
    """
    Options: --key-file and --password.  If `required` is True,
    --key-file is required.
    """

    def decorator(fn: Func) -> Func:
        return option(
            "--key-file", "-k", required=required, help="Encrypted private key file"
        )(
            option(
                "--password",
                "-p",
                help="Password for key file (or use env var 'KEYFILEPWD')",
            )(fn)
        )

    return decorator

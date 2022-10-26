"""
Configuration-related code
"""

import os
from click import ClickException
from getpass import getpass
from typing import Optional


KEYFILE_PASSWORD_ENV_VAR = "KEYFILEPWD"
WEB3_ENDPOINT_ENV_VAR = "WEB3_ENDPOINT"


def get_keyfile_password(
    password: Optional[str], key_file: Optional[str] = None
) -> str:
    """
    Get the keyfile password, given a cli parameter `password`.  Fall
    back to env vars if cli parameter is not given, then to user
    input.
    """

    # Read password
    if password is None:
        password = os.getenv(KEYFILE_PASSWORD_ENV_VAR)
        if password is None:
            password = getpass(
                "KEYFILEPWD env var not set (consider using 'KEYFILEPWD').\n"
                + "Enter passphrase "
                + ("" if key_file is None else f"for {key_file} ")
                + "(or CTRL-d to exit): "
            )

    return password


def get_rpc_endpoint(endpoint: Optional[str]) -> str:
    """
    Get the RPC endpoint configuration value, where param is the
    command-line option. If param is not given, check the env var,
    then configuration files, falling back to the default.
    """

    if endpoint is None:
        endpoint = os.getenv(WEB3_ENDPOINT_ENV_VAR)
        if endpoint is None:
            raise ClickException(
                f"rpc end-point not given (use cmd line param or {WEB3_ENDPOINT_ENV_VAR} env var"
            )

    return endpoint
